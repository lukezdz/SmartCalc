package com.example.smartcalcapp;

import android.content.Context;

import org.deeplearning4j.nn.multilayer.MultiLayerNetwork;
import org.deeplearning4j.util.ModelSerializer;
import org.nd4j.linalg.api.ndarray.INDArray;

import java.io.IOException;
import java.io.InputStream;
import java.util.Arrays;
import java.util.List;

public class NeuralNetwork {
    private final MultiLayerNetwork network;
    private final List<String> outputMapping;

    public NeuralNetwork(Context context) throws IOException {
        InputStream inputStream = context.getResources().openRawResource(R.raw.model);
        network = ModelSerializer.restoreMultiLayerNetwork(inputStream);

        outputMapping = Arrays.asList("0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                "a", "b", "c", "d", "e", "+", "-", "*", "/", "=", "(", ")");
    }

    public String predict(INDArray singleCharacter) {
        int[] answer = network.predict(singleCharacter);
        return outputMapping.get(answer[0]);
    }
}