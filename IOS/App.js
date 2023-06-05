import * as React from 'react';
import {
  StyleSheet,
  Button,
  View,
  SafeAreaView,
  Text,
  Alert,
} from 'react-native';
import Paho from 'paho-mqtt';

const Separator = () => <View style={styles.separator} />;

class App extends React.Component {
  componentDidMount() {
    global.client = new Paho.Client(
      'broker.hivemq.com',
      Number(8884),
      'testasdasd12312dfsd31'
    );
    client.onMessageArrived = function(message) {
      console.log('Topic: ' + message.destinationName + ", Message: " + message.payloadString)
    }

    client.connect({
      onSuccess: function() {
        console.log('connected');
        client.subscribe('aegisDongleSend');
        client.publish("aegisDongleReceive", "off", Number(0), false);
      },
      onFailure: function(err) {
        console.log(err.errorCode);
        console.log(err.errorMessage);
      },
      useSSL: true,
    });
  }
  
  render() {
    return (
      <SafeAreaView style={styles.container}>
      <View>
        <Button
          title="Off"
          onPress={this.sendOff}
        />
      </View>
      <Separator />
      <View>
        <Button
          title="on"
          onPress={this.sendOn}
        />
      </View>
    </SafeAreaView>
    );
  }
  sendOff() {
    client.publish("aegisDongleReceive", "off", Number(0), false);
    // alert('Off sent!');
  }
  sendOn() {
    client.publish("aegisDongleReceive", "on", Number(0), false);
    // alert('On sent!');
  }
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});
export default App;
