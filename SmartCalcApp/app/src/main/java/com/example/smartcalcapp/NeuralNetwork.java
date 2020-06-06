package com.example.smartcalcapp;

import android.content.Context;
import android.media.Image;
import android.os.Environment;

import org.deeplearning4j.nn.multilayer.MultiLayerNetwork;
import org.deeplearning4j.util.ModelSerializer;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;

import it.unimi.dsi.fastutil.objects.Reference2ByteOpenHashMap;

public class NeuralNetwork {
    private final MultiLayerNetwork network;

    public NeuralNetwork(Context context) throws IOException {
        InputStream inputStream = context.getResources().openRawResource(R.raw.model);
        network = ModelSerializer.restoreMultiLayerNetwork(file);
    }

    public String predict(Image image) {

    }
}
