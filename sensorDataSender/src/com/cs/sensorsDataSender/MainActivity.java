package com.cs.sensorsDataSender;

import java.text.DecimalFormat;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import com.cs.sensorsDataSender.R;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.SeekBar;
import android.widget.TextView;
import de.tavendo.autobahn.WebSocketConnection;
import de.tavendo.autobahn.WebSocketException;
import de.tavendo.autobahn.WebSocketHandler;

//TODO: ¿Delete all unused methods?
/**
 * @author mac
 *
 */
public class MainActivity extends Activity implements SensorEventListener {
	private static final String TAG = "Sensors: ";
	
	private float[] lastAccelerometer;
    private float[] lastMagnetometer;
    private SensorManager sensorManager;
	private Sensor accelerometer;
	private float gravity[] = new float[3];
	private Sensor magnetometer;
	private SeekBar frequencyChanger = null;
	private Button startBtn = null;
	private Button stopBtn = null;
	private int freqVal = 0;
	
    final WebSocketConnection websocket = new WebSocketConnection();
	private boolean emitEvents;
	
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		
		sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
		accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
		magnetometer = sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE);
		
		getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
		
		frequencyChanger = (SeekBar) findViewById(R.id.freq_ch);
		startBtn = (Button) findViewById(R.id.start);
		stopBtn = (Button) findViewById(R.id.stop);
		frequencyUpdater();
		
		emitEvents = false;
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

	protected void onResume() {
		super.onResume();
        sensorManager.registerListener(this, accelerometer, freqVal);
        sensorManager.registerListener(this, magnetometer, freqVal);
	}

	protected void onPause() {
		super.onPause();
		websocket.disconnect();
		sensorManager.unregisterListener(this);
	}
	
	public void onAccuracyChanged(Sensor sensor, int accuracy) {
	}

	public void onSensorChanged(SensorEvent event) {
		float realAcceleration[] = new float[3];
		float orientation[] = new float[3];
		if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER) {
			lastAccelerometer = event.values;
			final float alpha = (float) 0.8;
	        gravity[0] = alpha * gravity[0] + (1 - alpha) * event.values[0];
	        gravity[1] = alpha * gravity[1] + (1 - alpha) * event.values[1];
	        gravity[2] = alpha * gravity[2] + (1 - alpha) * event.values[2];	        
	        realAcceleration[0] = lastAccelerometer[0] - gravity[0];
	        realAcceleration[1] = lastAccelerometer[1] - gravity[1];
	        realAcceleration[2] = lastAccelerometer[2] - gravity[2];
	        displayEventData(realAcceleration, false);
	        if (emitEvents && websocket.isConnected()) {
				String response = "{\"acc\": ["+System.currentTimeMillis()+","
				   +realAcceleration[0]+","
				   +realAcceleration[1]+","
				   +realAcceleration[2]+"] }";
				websocket.sendTextMessage(response);
				Log.d(TAG, "Got echo: " + response);
	        }
		}
		
		if (event.sensor.getType() == Sensor.TYPE_GYROSCOPE) {
			lastMagnetometer = event.values;
			float rotationMatrix[] = new float[9];   
			boolean success = SensorManager.getRotationMatrix(rotationMatrix, null, lastAccelerometer, lastMagnetometer);
			if (success) {
				SensorManager.getOrientation(rotationMatrix, orientation);
				orientation[0] = (float)Math.toDegrees((double)orientation[0]);
				orientation[1] = (float)Math.toDegrees((double)orientation[1]);
				orientation[2] = (float)Math.toDegrees((double)orientation[2]);
			}
			displayEventData(orientation, true);
			if (emitEvents && websocket.isConnected()) {
				String response = "{\"gyr\": ["+System.currentTimeMillis()+","
				   +orientation[0]+","
				   +orientation[1]+","
				   +orientation[2]+"] }";
				websocket.sendTextMessage(response);
				Log.d(TAG, "Got echo: " + response);
			}
		}
	}
	
	/**
	 * Запуск считывания данных с датчиков
	 * @param view
	 */
    public void startEvents(View view) {

    	EditText editIp = (EditText) findViewById(R.id.ip_addr);
    	EditText editPort = (EditText) findViewById(R.id.port);
    	
    	String ipText = editIp.getText().toString().trim();
    	String portText = editPort.getText().toString().trim();
    	
    	boolean isCorrect = checkIpPort(ipText, portText);
    	
    	if (isCorrect) {
    		createConnection(ipText, portText);
    		startBtn.setEnabled(false);
    		stopBtn.setEnabled(true);
    		frequencyChanger.setEnabled(false);
    	}

    }
    
    /**
     * Остановка считывания данных с датчиков
     * @param view
     */
    public void stopEvents(View view) {
    	stopDataSending();
    }
    
    /**
     * Выход из программы
     * @param view
     */
    public void exit(View view) {
    	stopDataSending();
    	android.os.Process.killProcess(android.os.Process.myPid());
    	super.onDestroy();
    }
    
    /**
     * Создание соединения с сервером
     * @param ipText ip-адрес
     * @param portText порт
     */
    private void createConnection(String ipText, String portText) {
    	try {
//			final String url = "ws://192.168.1.28:3000/ws";
//    		final String url = "ws://178.62.197.146:3000/ws";
			final String url = "ws://"+ipText+":"+portText+"/ws";
			websocket.connect(url, new WebSocketHandler(){
            	@Override
                public void onOpen() {
                   Log.d(TAG, "Status: Connected to " + url);
                }
     
                @Override
                public void onTextMessage(String payload) {
                	if (payload.equals("whoIs")) {
                		websocket.sendTextMessage("{\"iAm\": \"sender\"}" );
        	    		if (!emitEvents) {
        	    			emitEvents = !emitEvents;
        	    			System.out.println("Emitting events.");
        	    		}
                	}
                   Log.d(TAG, "Got echo: " + payload);
                }
     
                @Override
                public void onClose(int code, String reason) {
                   Log.d(TAG, "Connection closed");
                }
            });
		} catch (WebSocketException e) {
			e.printStackTrace();
		}
    	
    }

    /**
     * Проверка корректности ip-адреса и порта
     * @param ipText ip-адрес
     * @param portText порт
     * @return True если оба знаыения корректно введены, иначе False
     */
    private boolean checkIpPort(String ipText, String portText){
    	boolean isCorrect = true;
    	final AlertDialog alertDialog = new AlertDialog.Builder(this).create();
		alertDialog.setTitle(R.string.attention);
		alertDialog.setButton(DialogInterface.BUTTON_NEUTRAL, "OK", new DialogInterface.OnClickListener() {
 		   public void onClick(DialogInterface dialog, int which) {
 			   alertDialog.cancel();
 		   }
 		});
    	if (accelerometer == null || magnetometer == null) {

			alertDialog.setMessage("Отсутствуют необходимые датчики на мобильном устройстве");   		
			alertDialog.show();
			return false;
		}
    	String regexIp = "^(25[0-5]|2[0-4]\\d|[0-1]\\d{2}|\\d{2}|\\d)(\\.(25[0-5]|2[0-4]\\d|[0-1]\\d{2}|\\d{2}|\\d)){3}$";
    	Pattern patternIp = Pattern.compile(regexIp);
    	Matcher matcherIp = patternIp.matcher(ipText);
    	
    	String regexPort = "^(1((0((2[4-9])|([3-9]\\d)))|([1-9]\\d{2})))|"+
    					   "(6(([0-4]\\d{3})|(5(([0-4]\\d{2})|(5(([0-2]\\d)|(3[0-5])))))))|"+
    					   "([1-5]\\d{4})|"+
    					   "([2-9]\\d{3})$";
    	Pattern patternPort = Pattern.compile(regexPort);
    	Matcher matcherPort = patternPort.matcher(portText);
    	
    	String errorMessage = "";
    	if (!matcherIp.matches()) {
    		errorMessage = "Не корректно введен ip-адрес";
    		isCorrect = false;
    	}
    	
    	if (!matcherPort.matches())
    	{ 
    		if (!isCorrect) {
    			errorMessage = "Не корректно введен ip-адрес и порт";
    		}
    		else {
    			errorMessage = "Не корректно введен порт";
    		}
    		isCorrect = false;
    	}
    	
    	if (!isCorrect) {
    		alertDialog.setMessage(errorMessage);   		
    		alertDialog.show();
    	}
    	
    	return isCorrect;
    }
	
    /**
     * Вывод текущих данных датчиков на экран
     * @param data данные датчика
     * @param type True если данные гироскопа, False если акселерометра
     */
    private void displayEventData(float data[], boolean type) {
    	DecimalFormat df = new DecimalFormat();
		df.setMaximumFractionDigits(4);
		TextView txtViewAx = (TextView) findViewById(R.id.ax);
		TextView txtViewAy = (TextView) findViewById(R.id.ay);
		TextView txtViewAz = (TextView) findViewById(R.id.az);
		if (!type) {
			txtViewAx.setText(df.format(data[0]));
			txtViewAy.setText(df.format(data[1]));
			txtViewAz.setText(df.format(data[2]));
		}
		
		TextView txtViewGx = (TextView) findViewById(R.id.gx);
		TextView txtViewGy = (TextView) findViewById(R.id.gy);
		TextView txtViewGz = (TextView) findViewById(R.id.gz);
		if (type) {
			txtViewGx.setText(df.format(data[0]%1));
			txtViewGy.setText(df.format(data[1]%1));
			txtViewGz.setText(df.format(data[2]%1));
		}
    }

    /**
     * Изменение частоты считывания данных
     */
    private void frequencyUpdater() {
    	sensorManager.unregisterListener(this, accelerometer);
    	sensorManager.unregisterListener(this, magnetometer);
    	
		frequencyChanger.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener(){

		    @Override
		    public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
		    	freqVal = seekBar.getMax() - progress;
		    	displayFreqData();
		    }

		    @Override
		    public void onStartTrackingTouch(SeekBar seekBar) {

		    }

		    @Override
		    public void onStopTrackingTouch(SeekBar seekBar) {

		    }
		});
    }
    
    /**
     * Вывод частоты считывания данных
     */
    private void displayFreqData() {
    	final TextView freqText = (TextView) findViewById(R.id.freq_val);
    	sensorManager.registerListener(this, accelerometer, freqVal);
        sensorManager.registerListener(this, magnetometer, freqVal);
    	switch (freqVal) {
    	case 3: freqText.setText("5");break;
    	case 2: freqText.setText("15");break;
    	case 1: freqText.setText("50");break;
    	case 0: freqText.setText("100");break;
    	}
    }
    
    /**
     * Остановка передачи данных на сервер
     */
    private void stopDataSending(){
    	if (emitEvents) {
    		emitEvents = !emitEvents;
    		websocket.disconnect();
    		System.out.println("Stopped emitting events.");
    		startBtn.setEnabled(true);
    		stopBtn.setEnabled(false);
    		frequencyChanger.setEnabled(true);
    	}
    }
}
