package com.example.smartcalcapp;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.Manifest;
import android.app.ActivityManager;
import android.content.pm.PackageManager;
import android.graphics.Camera;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;

public class MainActivity extends AppCompatActivity {
    private static final List<String> permissions = Arrays.asList(
            Manifest.permission.CAMERA
    );
    private static final int permissionRequestCode = 34;
    private boolean isCameraInitialized = false;
    private Camera camera = null;
    private Engine engine = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        try {
            engine = new Engine(getApplicationContext());
        }
        catch (IOException exception) {
            Log.e("Failed to create engine", exception.getMessage());
        }
        setContentView(R.layout.activity_main);
    }

    // get the camera working and stuff
}
