//
//  ContentView.swift
//  AEGIS
//
//  Created by Emin Tunc Kirimlioglu on 6/5/23.
//
//

import SwiftUI
import CoreData
import CocoaMQTT

class Room: ObservableObject, Identifiable {
    let id = UUID()
    @Published var dongleAddress: String = ""
    @Published var name: String = ""
    @Published var temperature: String = ""
    @Published var humidity: String = ""
    @Published var current: String = ""
}


struct ContentView: View {
    @State private var isOn = true
    @ObservedObject var mqttDelegate = MQTTDelegate()

    var mqtt: CocoaMQTT

    init() {
        self.mqtt = CocoaMQTT(clientID: "aegisAppb895eb67", host: "aegishome.ninja", port: 8003)
                mqtt.username = "aegisAdmin"
                mqtt.password = "iLoveAegis!"
                mqtt.delegate = mqttDelegate
    }
    
    var body: some View {
        GeometryReader { geometry in
        VStack {
            Text("House Information")
                .font(.system(size: 30))
                .padding(.top, 5)
                
            
                List(mqttDelegate.rooms) { room in
                    VStack(alignment: .leading) {
                        Text("Room: \(room.name)")
                        Text("Temperature: \(room.temperature)")
                        Text("Humidity: \(room.humidity)")
                        Text("Current: \(room.current)")
                        Button(action: {
                            mqttDelegate.activeID = room.dongleAddress
                                        mqttDelegate.activename = room.name
                                        mqttDelegate.activetemp = room.temperature
                                        mqttDelegate.activehum = room.humidity
                                        mqttDelegate.activecurrent = room.current
                                    }) {
                                        Text("Activate Room")
                        }
                    }
                }
            
            Text("Currently Controlling the Room: \(mqttDelegate.activename)")
                            .font(.system(size: 30))
                            .padding(.bottom, 15)

                        Text("Set temperature: \(mqttDelegate.activeSetTemp)°C")
                            .font(.system(size: 20))
                            .padding(.bottom, 5)
                        
                        HStack(spacing: 20) {
                            Button(action: {
                                // Increase the temperature in your app:
                                if let currentTemp = Int(mqttDelegate.activeSetTemp) {
                                    mqttDelegate.activeSetTemp = String(currentTemp + 1)
                                }
                                self.mqtt.publish("Aegis/aegisTempSet", withString: "\(mqttDelgate.activename),\(mqttDelegate.activeSetTemp)")
                            }) {
                                Text("Increase Temp")
                            }
                            .buttonStyle(.bordered)
                            Button(action: {
                                // Decrease the temperature in your app:
                                if let currentTemp = Int(mqttDelegate.activeSetTemp) {
                                    mqttDelegate.activeSetTemp = String(currentTemp - 1)
                                }
                                self.mqtt.publish("Aegis/aegisTempSet", withString: "\(mqttDelgate.activename),\(mqttDelegate.activeSetTemp)")
                            }) {
                                Text("Decrease Temp")
                            }
                            .buttonStyle(.bordered)
                        
                        }
                        .padding(.top, 14)
            
                        HStack(spacing:20){
                            Button(action: {
                                self.isOn = true
                                self.mqtt.publish("Aegis/aegisDongleReceive/\(mqttDelegate.activeID)", withString: "on")
                            }) {
                                Text("On")
                            }
                            .buttonStyle(.bordered)

                            Button(action: {
                                self.isOn = false
                                self.mqtt.publish("Aegis/aegisDongleReceive/\(mqttDelegate.activeID)", withString: "off")
                            }) {
                                Text("Off")
                            }
                            .buttonStyle(.bordered)
                        }.padding(.top,14).padding(.bottom,30)

                        
                        Text(mqttDelegate.message)
                            .padding(.bottom, 10)
        }
        .frame(height: geometry.size.height*1.0)
    }
        .onAppear {
            mqtt.connect()
        }
    }
}



class MQTTDelegate: NSObject, ObservableObject, CocoaMQTTDelegate {
    @Published var rooms = [Room]()
    @Published var message: String = ""
    @Published var activeID: String = ""
    @Published var activename: String = ""
    @Published var activeSetTemp: String = "70"
    @Published var activetemp: String = ""
    @Published var activehum: String = ""
    @Published var activecurrent: String = ""
    
    func mqtt(_ mqtt: CocoaMQTT, didConnectAck ack: CocoaMQTTConnAck) {
        message = "Connected"
        mqtt.subscribe("Aegis/aegisDongleSend/#")
        mqtt.subscribe("Aegis/aegisTempSet")
    }
    
    func mqtt(_ mqtt: CocoaMQTT, didPublishMessage message: CocoaMQTTMessage, id: UInt16) {
        self.message = "Published"
    }
    
    func mqtt(_ mqtt: CocoaMQTT, didPublishAck id: UInt16) {
        self.message = "Published"
    }
    
    func mqtt(_ mqtt: CocoaMQTT, didReceiveMessage message: CocoaMQTTMessage, id: UInt16 ) {
        guard let payload = message.string else {
            return
        }
        let topic = message.topic.components(separatedBy: "/").last
        if topic == "aegisTempSet" {
            mqttDelegate.activeSetTemp = message.string.components(separatedBy: ",").last
            return
        } 
        let data = payload.split(separator: ";")
        let deviceId = topic
        if let lastData = data.last {
            let readings = lastData.split(separator: ",")
            if readings.count == 4 {
                let room = Room()
                room.name = String(readings[0])
                room.temperature = String(readings[1])
                room.humidity = String(readings[2])
                room.current = String(readings[3])
                if let index = rooms.firstIndex(where: { $0.name == room.name }) {
                    let newRoom = Room()
                    if let unwrapped = deviceId{
                        newRoom.dongleAddress = unwrapped
                    }
                    newRoom.name = room.name
                    newRoom.temperature = room.temperature
                    newRoom.humidity = room.humidity
                    newRoom.current = room.current
                    rooms[index] = newRoom  // Replacing the old Room object with a new one
                }
                else{
                    rooms.append(room)
                }
                
            }
        }
    }
    
    func mqtt(_ mqtt: CocoaMQTT, didSubscribeTopics success: NSDictionary, failed: [String]) {
        self.message = "Subscribed"
    }
    
    func mqtt(_ mqtt: CocoaMQTT, didUnsubscribeTopics topics: [String]) {
        self.message = "Unsubscribed"
    }
    
    func mqttDidPing(_ mqtt: CocoaMQTT) {}
    
    func mqttDidReceivePong(_ mqtt: CocoaMQTT) {}
    
    func mqttDidDisconnect(_ mqtt: CocoaMQTT, withError err: Error?) {
        if let error = err {
            message = error.localizedDescription
        } else {
            message = "Disconnected"
        }
    }
}

