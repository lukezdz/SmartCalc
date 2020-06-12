package com.example.smartcalcapp;

import android.content.Context;

import org.nd4j.linalg.api.ndarray.INDArray;
import org.nd4j.linalg.cpu.nativecpu.NDArray;
import org.opencv.core.Mat;
import org.opencv.core.MatOfPoint;
import org.opencv.core.MatOfPoint2f;
import org.opencv.core.Rect;
import org.opencv.core.Size;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;

import java.util.ArrayList;
import java.util.List;

public class Engine {
    private final NeuralNetwork neuralNetwork;

    public Engine(Context context) throws Exception {
        neuralNetwork = new NeuralNetwork(context);
    }

    public String getEquation(String filename) {
        Mat src = Imgcodecs.imread(filename);
        Mat srcGray = new Mat();
        Imgproc.cvtColor(src, srcGray, Imgproc.COLOR_BGR2GRAY);
        Imgproc.blur(srcGray, srcGray, new Size(3, 3));

        // using opencv cut image into bounding rects
        List<MatOfPoint> contours = new ArrayList<>();
        Mat hierarchy = new Mat();
        Imgproc.findContours(srcGray, contours, hierarchy, Imgproc.RETR_TREE, Imgproc.CHAIN_APPROX_SIMPLE);

        List<Rect> boundingRectangles = new ArrayList<>();
        List<MatOfPoint2f> contoursPoly  = new ArrayList<>();
        for (int i = 0; i < contours.size(); i++) {
            contoursPoly.add(new MatOfPoint2f());
            Imgproc.approxPolyDP(new MatOfPoint2f(contours.get(i).toArray()), contoursPoly.get(i), 3, true);
            boundingRectangles.add(Imgproc.boundingRect(new MatOfPoint(contoursPoly.get(i).toArray())));
        }

        StringBuilder equationBuilder = new StringBuilder();
        for (Rect rectangle : boundingRectangles) {
            // get data from rect
            Mat cropped = srcGray.submat(rectangle);
            // rescale to 28x28
            Mat resized = new Mat();
            Imgproc.resize(cropped, resized, new Size(28, 28));
            // reshape this to 784x1 NDArray using this.reshape(rescaledImage)
            INDArray reshaped = reshape(resized);
            // predict single character and add ans to return equation
            String prediction = neuralNetwork.predict(reshaped);
            equationBuilder.append(prediction);
        }
        return equationBuilder.toString();
    }

    private INDArray reshape(Mat image) {
        // fill in values with data from image
        int [] values = new int[784];
        int [] shape = {784, 1};

        for (int y = 0; y < image.height(); y++) {
            for (int x = 0; x < image.width(); x++) {
                values[x + y * image.width()] = (int)image.get(y, x)[0];
            }
        }

        return new NDArray(values, shape, 0);
    }
}
