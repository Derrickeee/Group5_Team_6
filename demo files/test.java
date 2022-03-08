package com.example.x08part2;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;

import java.util.ArrayList;
import java.util.List;

/* This is a comment */

/*
asdas
asdasdasasdjh
WOOOOOOO
*/

// Comment

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        int i = fun(10);
        android.util.Log.i("MYINT", "value: " + i);
	Log.d("TAG", "this");
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public int fun(int n) {
        //  Block of code to handle errors
        int i = 0, j = 0;
        int tmp = 0;
        for (i = 0; i < n; i++) {
            for (j = 0; j < n; j++) {
                tmp = tmp + j;
                System.out.println("Hello World");
            }
        }

        return tmp;
    }
}