package com.cnfs.contador;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;

public class MainActivity extends Activity {
    private int count;
    private TextView counter;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        SharedPreferences p = getSharedPreferences("contador", MODE_PRIVATE);
        count = p.getInt("count", 0);
        counter = findViewById(R.id.counter);
        counter.setText(String.valueOf(count));
        Button plus = findViewById(R.id.btn_plus);
        Button about = findViewById(R.id.btn_about);
        plus.setOnClickListener(v -> {
            count++;
            counter.setText(String.valueOf(count));
            p.edit().putInt("count", count).apply();
        });
        about.setOnClickListener(v ->
            startActivity(new Intent(MainActivity.this, AboutActivity.class)));
    }
}
