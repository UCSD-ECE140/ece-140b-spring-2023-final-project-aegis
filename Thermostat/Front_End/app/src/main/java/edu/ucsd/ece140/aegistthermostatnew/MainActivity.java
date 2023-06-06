package edu.ucsd.ece140.aegistthermostatnew;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

import android.provider.Settings;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.hivemq.client.mqtt.MqttClient;
import com.hivemq.client.mqtt.mqtt3.Mqtt3AsyncClient;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Vector;

public class MainActivity extends AppCompatActivity {

    static String theActiveRoom = "Living Room";
    String theFanStatus = "Auto";
    String theSystemStatus = "Off";
    String theDecision = "Cooling will start in 5 minutes";
    String currHumidity = "50%";
    static String currIn = "73";
    String currOut = "72";
    String currTarget = "74";

    HashMap<String,Integer> rooms = new HashMap<>();


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);

        setContentView(R.layout.activity_main);

        RecyclerView recyclerView = findViewById(R.id.recyclerView);
        recyclerView.setHasFixedSize(true);


        //spawn a thread that updates the UI every 0.5 seconds
        Thread t = new Thread() {
            @Override
            public void run() {
                try {
                    while (!isInterrupted()) {
                        Thread.sleep(500);
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                TextView activeRoom = findViewById(R.id.activeRoom);
                                activeRoom.setText(theActiveRoom);

                                TextView fanStatus = findViewById(R.id.fanStatus);
                                fanStatus.setText(theFanStatus);

                                TextView systemStatus = findViewById(R.id.SystemStatus);
                                systemStatus.setText(theSystemStatus);

                                TextView decision = findViewById(R.id.theThought);
                                decision.setText(theDecision);
                            }
                        });
                    }
                } catch (InterruptedException e) {
                }
            }
        };

        t.start();

        LinearLayoutManager layoutManager = new LinearLayoutManager(this);
        recyclerView.setLayoutManager(layoutManager);

        Vector<Room> rooms = new Vector<>();
        roomAdapter adapter = new roomAdapter(rooms);
        recyclerView.setAdapter(adapter);

        Room demoRoom = new Room();
        demoRoom.id = "001";
        demoRoom.name = "Living Room";
        demoRoom.temperature = 73;
        rooms.add(demoRoom);
        this.rooms.put(demoRoom.id,0);

        demoRoom = new Room();
        demoRoom.id = "002";
        demoRoom.name = "Bedroom";
        demoRoom.temperature = 74;
        rooms.add(demoRoom);
        this.rooms.put(demoRoom.id,1);

        demoRoom = new Room();
        demoRoom.id = "003";
        demoRoom.name = "Kitchen";
        demoRoom.temperature = 72;
        rooms.add(demoRoom);
        this.rooms.put(demoRoom.id,2);


        ImageView plus = findViewById(R.id.plus);
        ImageView minus = findViewById(R.id.minus);

        String androidId = Settings.Secure.getString(
                getContentResolver(),
                Settings.Secure.ANDROID_ID);


        Mqtt3AsyncClient client = MqttClient.builder()
                .useMqttVersion3()
                .identifier("aegisApp"+androidId.substring(androidId.length()-6))
                .serverHost("broker.hivemq.com")
                .serverPort(1883)
                .buildAsync();

        client.connect()
                .whenComplete((connAck, throwable) -> {
                    if (throwable != null) {
                        Log.d("MQTT", throwable.getMessage());
                    } else {
                        Log.d("MQTT", "Connected");
                    }
                });

        plus.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
               int curr = Integer.parseInt(currTarget);
               if(curr < 90) {
                   curr++;
               }
               currTarget = Integer.toString(curr);
                client.publishWith()
                        .topic("aegisThermostatSet")
                        .payload(currTarget.getBytes())
                        .send()
                        .whenComplete((publish, throwable) -> {
                            if (throwable != null) {
                                Log.d("MQTT", throwable.getMessage());
                            } else {
                                Log.d("MQTT", "Published");
                            }
                        });
                TempDialView tempDialView = findViewById(R.id.tempDialView);
                tempDialView.setValue(tempDialView.indoor,tempDialView.outdoor,curr,tempDialView.humidity);
            }
        });
        minus.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                int curr = Integer.parseInt(currTarget);
                if(curr > 60) {
                    curr--;
                }
                currTarget = Integer.toString(curr);
                client.publishWith()
                        .topic("aegisThermostatSet")
                        .payload(currTarget.getBytes())
                        .send()
                        .whenComplete((publish, throwable) -> {
                            if (throwable != null) {
                                Log.d("MQTT", throwable.getMessage());
                            } else {
                                Log.d("MQTT", "Published");
                            }
                        });
                TempDialView tempDialView = findViewById(R.id.tempDialView);
                tempDialView.setValue(tempDialView.indoor,tempDialView.outdoor,curr,tempDialView.humidity);
            }
        });



        client.subscribeWith()
                .topicFilter("aegisDongleSend")
                .callback(publish -> {
                    if(publish.getPayload().isPresent()){
                        if(publish.getPayloadAsBytes().length < 6){
                            return;
                        }
                        String payload = new String(publish.getPayloadAsBytes());
                        String[] datas = payload.split(";");
                        String[] data = datas[datas.length-1].split(",");
                        if(this.rooms.containsKey(data[0])){
                            rooms.get(this.rooms.get(data[0])).temperature = Integer.parseInt(data[1]);
                            rooms.get(this.rooms.get(data[0])).humidity = Integer.parseInt(data[2]);
                            adapter.notifyDataSetChanged();
                            TempDialView tempDialView = findViewById(R.id.tempDialView);
                            tempDialView.setValue(Integer.parseInt(data[1]),tempDialView.outdoor,
                                    tempDialView.setTo,Integer.parseInt(data[2]));
                        }

                    }
                })
                .send()
                .whenComplete((subAck, throwable) -> {
                    if (throwable != null) {
                        Log.d("MQTT", throwable.getMessage());
                    } else {
                        Log.d("MQTT", "Subscribed");
                    }});


    }

    static void setRoomAsMain(String info) {
        // Code here to set the specified room as the main control point
        String[] infos = info.split(",");
        theActiveRoom = infos[0];
        currIn = infos[1];

    }
}