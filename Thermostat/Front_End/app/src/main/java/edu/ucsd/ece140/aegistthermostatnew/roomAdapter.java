package edu.ucsd.ece140.aegistthermostatnew;

import static edu.ucsd.ece140.aegistthermostatnew.MainActivity.setRoomAsMain;

import android.view.*;
import android.widget.Button;
import android.widget.TextView;
import androidx.recyclerview.widget.RecyclerView;

import java.util.List;

public class roomAdapter extends RecyclerView.Adapter<roomAdapter.MyViewHolder> {
    private List<Room> rooms;

    public static class MyViewHolder extends RecyclerView.ViewHolder {
        public TextView roomName;
        public TextView temperature;

        public MyViewHolder(View v) {
            super(v);
            roomName = v.findViewById(R.id.roomName);
            temperature = v.findViewById(R.id.temperature);
        }
    }

    public roomAdapter(List<Room> rooms) {
        this.rooms = rooms;
    }

    @Override
    public roomAdapter.MyViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.roominfo, parent, false);
        return new MyViewHolder(v);
    }

    @Override
    public void onBindViewHolder(MyViewHolder holder, int position) {
        Room room = rooms.get(position);
        holder.roomName.setText(room.name);
        holder.temperature.setText(String.valueOf(room.temperature));
        // Get the button for this layout
        Button setAsMainButton = holder.itemView.findViewById(R.id.setAsMain);

        // Attach the room ID as the button's tag
        String totalName = "";
        totalName+=room.name + "," + room.temperature;
        setAsMainButton.setTag(totalName);

        // Set the click listener
        setAsMainButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                // Retrieve the tag
                String roomInfo = (String) v.getTag();

                // Now you know which room's button was clicked!
                setRoomAsMain(roomInfo);
            }
        });
    }

    @Override
    public int getItemCount() {
        return rooms.size();
    }
}
