package edu.ucsd.ece140.aegistthermostatnew;
public class Room {
    public String name;
    public String id;
    public double humidity;
    public double temperature;
    public double targetTemperature;


    public Room() {
    }

    public String getId() {
        return id;
    }
}