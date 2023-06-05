//
//  ContentView.swift
//  AegisIOS
//
//  Created by Emin Tunc Kirimlioglu on 6/5/23.
//
//
import SwiftUI
import CocoaMQTT

struct ContentView: View {
    @State private var isOn = true
    @ObservedObject var mqttDelegate = MQTTDelegate()

    var mqtt: CocoaMQTT

    init() {
        self.mqtt = CocoaMQTT(clientID: "aegisAppb895eb67", host: "aegishome.ninja", port: 8003, username: "aegisAdmin", password: "iLoveAegis!")
        mqtt.delegate = mqttDelegate
    }
    
    var body: some View {
        VStack {
            Text("House Information")
                .font(.system(size: 30))
                .padding(.top, 16)
                
            HStack {
                Text("Temperature:")
                    .font(.system(size: 20))
                Spacer()
                Text(mqttDelegate.temp)
                    .font(.system(size: 20))
                    .padding(.leading, 144)
            }
            .padding(.top, 23)
            
            HStack {
                Text("Humidity:")
                    .font(.system(size: 20))
                Spacer()
                Text(mqttDelegate.hum)
                    .font(.system(size: 20))
                    .padding(.leading, 112)
            }
            .padding(.top, 7)
            
            HStack {
                Text("Current:")
                    .font(.system(size: 20))
                Spacer()
                Text(mqttDelegate.curr)
                    .font(.system(size: 20))
                    .padding(.leading, 92)
            }
            .padding(.top, 11)
            
            Text("Control The Outlet")
                .font(.system(size: 30))
                .padding(.bottom, 10)
            
            HStack {
                Button(action: {
                    self.isOn = true
                    self.mqtt.publish("aegisDongleReceive", withString: "on")
                }) {
                    Text("On")
                }
                .padding(.trailing, 24)
                
                Button(action: {
                    self.isOn = false
                    self.mqtt.publish("aegisDongleReceive", withString: "off")
                }) {
                    Text("Off")
                }
            }
            .padding(.top, 240)
            
            Spacer()
            
            Text(mqttDelegate.message)
                .padding(.bottom, 50)
        }
        .onAppear {
            mqtt.connect()
        }
    }
}

class MQTTDelegate: NSObject, ObservableObject, CocoaMQTTDelegate {
    @Published var message: String = ""
    @Published var temp: String = ""
    @Published var hum: String = ""
    @Published var curr: String = ""
    
    func mqtt(_ mqtt: CocoaMQTT, didConnectAck ack: CocoaMQTTConnAck) {
        message = "Connected"
        mqtt.subscribe("aegisDongleSend")
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
        
        let data = payload.split(separator: ";")
        
        if let lastData = data.last {
            let readings = lastData.split(separator: ",")
            if readings.count == 3 {
                temp = String(readings[0])
                hum = String(readings[1])
                curr = String(readings[2])
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

