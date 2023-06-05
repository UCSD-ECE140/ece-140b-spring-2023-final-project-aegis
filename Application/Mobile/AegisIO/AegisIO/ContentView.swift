//
//  ContentView.swift
//  AegisIO
//
//  Created by Emin Tunc Kirimlioglu on 5/30/23.
//
//
import SwiftUI
import CocoaMQTT

struct ContentView: View {
    @State private var isOn = true
    @State private var temp: String = "0.0C"
    @State private var hum: String = "0.0%"
    @State private var curr: String = "0.0A"
    @State private var message: String = "TextView"

    var mqtt: CocoaMQTT

    init() {
        self.mqtt = CocoaMQTT(clientID: "aegisAppb895eb67", host: "broker.hivemq.com", port: 1883)
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
                Text(temp)
                        .font(.system(size: 20))
                        .padding(.leading, 144)
            }
                    .padding(.top, 23)

            HStack {
                Text("Humidity:")
                        .font(.system(size: 20))
                Spacer()
                Text(hum)
                        .font(.system(size: 20))
                        .padding(.leading, 112)
            }
                    .padding(.top, 7)

            HStack {
                Text("Current:")
                        .font(.system(size: 20))
                Spacer()
                Text(curr)
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

            Text(message)
                    .padding(.bottom, 50)
        }
                .onAppear {
                    mqtt.delegate = self
                    mqtt.connect()
                }
    }
}

extension ContentView: CocoaMQTTDelegate {
    func mqtt(_ mqtt: CocoaMQTT, didConnect host: String, port: Int) {
        message = "Connected"
        mqtt.subscribe("aegisDongleSend")
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

    func mqtt(_ mqtt: CocoaMQTT, didPublishMessage message: CocoaMQTTMessage, id: UInt16) {
        self.message = "Published"
    }

    func mqtt(_ mqtt: CocoaMQTT, didPublishAck id: UInt16) {
        self.message = "Published"
    }

    func mqtt(_ mqtt: CocoaMQTT, didSubscribeTopic topics: [String]) {
        self.message = "Subscribed"
    }

    func mqtt(_ mqtt: CocoaMQTT, didUnsubscribeTopic topic: String) {
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


