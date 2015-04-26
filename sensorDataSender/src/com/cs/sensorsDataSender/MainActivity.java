package com.cs.sensorsDataSender;

import io.socket.*;

//import java.net.MalformedURLException;
//import java.net.URI;
import java.util.regex.Matcher;
import java.util.regex.Pattern;




//import org.java_websocket.WebSocket;
import org.json.*;

import com.cs.sensorsDataSender.R;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.view.WindowManager;
import android.widget.EditText;
import de.tavendo.autobahn.WebSocketConnection;
import de.tavendo.autobahn.WebSocketException;
import de.tavendo.autobahn.WebSocketHandler;

//TODO: ¿Delete all unused methods?
public class MainActivity extends Activity implements IOCallback, SensorEventListener, LocationListener {
	private static final String TAG = "Sensors: ";
	
	private float[] lastAccelerometer;
    //private float[] lastMagnetometer;

    private SensorManager sensorManager;
	private Sensor accelerometer;
	private LocationManager locationManager;
	private float gravity[] = new float[3];
	//private Sensor magnetometer;
	static final float NS2S = 1.0f / 1000000000.0f;
	
    final WebSocketConnection websocket = new WebSocketConnection();
	private boolean emitEvents;
	
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		
		sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
		
		accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
		locationManager = (LocationManager)getSystemService(LOCATION_SERVICE);
		
		locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 0, 0, this);

		//magnetometer = sensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD);
		
		getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
		
		emitEvents = false;
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

	protected void onResume() {
		super.onResume();
        sensorManager.registerListener(this, accelerometer, SensorManager.SENSOR_DELAY_FASTEST);
        //sensorManager.registerListener(this, magnetometer, SensorManager.SENSOR_DELAY_FASTEST);
	}

	protected void onPause() {
		super.onPause();
		websocket.disconnect();
		sensorManager.unregisterListener(this);
		locationManager.removeUpdates(this);
	}
	
	public void onAccuracyChanged(Sensor sensor, int accuracy) {
	}

	public void onSensorChanged(SensorEvent event) {
		if (emitEvents && websocket.isConnected()) {
			if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER)
				lastAccelerometer = event.values;
			
			
			//if (event.sensor.getType() == Sensor.TYPE_MAGNETIC_FIELD)
			//	lastMagnetometer = event.values;
			
			if (lastAccelerometer != null) { // && lastMagnetometer != null) {
				final float alpha = (float) 0.8;
//				float gravity[] = new float[3];
				float realAcceleration[] = new float[3];
		        gravity[0] = alpha * gravity[0] + (1 - alpha) * event.values[0];
		        gravity[1] = alpha * gravity[1] + (1 - alpha) * event.values[1];
		        gravity[2] = alpha * gravity[2] + (1 - alpha) * event.values[2];
		        
		        realAcceleration[0] = lastAccelerometer[0] - gravity[0];
		        realAcceleration[1] = lastAccelerometer[1] - gravity[1];
		        realAcceleration[2] = lastAccelerometer[2] - gravity[2];
		        /*
		        float rotationMatrix[] = new float[9];
				   
				boolean success = SensorManager.getRotationMatrix(rotationMatrix, null, lastAccelerometer, lastMagnetometer);
		        
				if (success) {
					float orientation[] = new float[3];
					SensorManager.getOrientation(rotationMatrix, orientation);
				
					orientation[0] = (float)Math.toDegrees((double)orientation[0]);
					orientation[1] = (float)Math.toDegrees((double)orientation[1]);
					orientation[2] = (float)Math.toDegrees((double)orientation[2]);
					String response = "{\"sCh\": ["+System.currentTimeMillis()+","
							   					   +realAcceleration[0]+","
							   					   +realAcceleration[1]+","
												   +realAcceleration[2]+","
												   +orientation[0]+","
												   +orientation[1]+","
												   +orientation[2]+"] }";
				*/
//		        	String response = "{\"sCh\": ["+System.currentTimeMillis()+","
		        	String response = "{\"sCh\": ["+event.timestamp*NS2S+","
	   					   +realAcceleration[0]+","
	   					   +realAcceleration[1]+","
						   +realAcceleration[2]+"] }";

					websocket.sendTextMessage(response);
					Log.d(TAG, "Got echo: " + response);
				//}
			}
		}
	}

    public void onMessage(JSONObject json, IOAcknowledge ack) {
        try {
            System.out.println("Server said:" + json.toString(2));
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    public void onMessage(String data, IOAcknowledge ack) {
        System.out.println("Server said: " + data);
    }

    public void onError(SocketIOException socketIOException) {
        System.out.println("an Error occured");
        socketIOException.printStackTrace();
    }

    public void onDisconnect() {
//    	websocket.disconnect();
        System.out.println("Connection terminated.");
    }

    public void onConnect() {
        System.out.println("Connection established");
    }

    public void on(String event, IOAcknowledge ack, Object... args) {
        System.out.println("Server triggered event '" + event + "'");
    	if (event.equals("whoIs")) {
    		websocket.sendTextMessage("{\"iAm\": \"viewer\"}" );
    	}
    }
    
    public void startEvents(View view) {
    	
//    	EditText editIP = (EditText) findViewById(R.id.ip_addr);
//    	String regex = "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)."+
//    				   "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)."+
//    				   "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)."+
//    				   "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)";
//    	Pattern p = Pattern.compile(regex);
//    	Matcher m = p.matcher(editIP.getText());
    	final AlertDialog alertDialog = new AlertDialog.Builder(this).create();
		alertDialog.setTitle(R.string.error);
		alertDialog.setButton(DialogInterface.BUTTON_NEUTRAL, "OK", new DialogInterface.OnClickListener() {
 		   public void onClick(DialogInterface dialog, int which) {
 			   alertDialog.cancel();
 		   }
 		});
//    	if (m.matches())
	    	if (accelerometer != null) {// && magnetometer != null) {
	    			createConnection();//editIP.getText().toString());
	    	}
	    	else {
	    		alertDialog.setMessage("Отсутствуют необходимые датчики на мобильном устройстве");   		
	    		alertDialog.show();
	    	}
//    	else {
//    		alertDialog.setMessage("Не корректно введен IP адрес");   		
//    		alertDialog.show();
//    	}
    }
    
    public void stopEvents(View view) {
    	if (emitEvents) {
    		emitEvents = !emitEvents;
    		websocket.disconnect();
    		System.out.println("Stopped emitting events.");
    	}
    }
    
    private void createConnection() {//String ip) {
    	try {
			//final String url = "ws://192.168.1.28:3000/ws";
			//final String url = "ws://"+ip+":3000/ws";
    		final String url = "ws://178.62.197.146:3000/ws";
			websocket.connect(url, new WebSocketHandler(){
            	@Override
                public void onOpen() {
                   Log.d(TAG, "Status: Connected to " + url);
                }
     
                @Override
                public void onTextMessage(String payload) {
                	if (payload.equals("whoIs")) {
                		websocket.sendTextMessage("{\"iAm\": \"viewer\"}" );
        	    		if (!emitEvents) {
        	    			emitEvents = !emitEvents;
        	    			System.out.println("Emitting events.");
        	    		}
                	}
                   Log.d(TAG, "Got echo: " + payload);
                }
     
                @Override
                public void onClose(int code, String reason) {
                   Log.d(TAG, "Connection lost.");
                }
            });
		} catch (WebSocketException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    	
    }

	@Override
	public void onLocationChanged(Location location) {
		// TODO Auto-generated method stub
		if (location != null) 
	       {
	          Log.d(TAG, "Широта="+location.getLatitude());
	          Log.d(TAG, "Долгота="+location.getLongitude());
	       }
		//Log.d("Location", location.getAltitude() + "|" + location.getLatitude() + "|" + location.getLongitude());
		
	}

	@Override
	public void onProviderDisabled(String provider) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onProviderEnabled(String provider) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onStatusChanged(String provider, int status, Bundle extras) {
		// TODO Auto-generated method stub
		
	}
}
