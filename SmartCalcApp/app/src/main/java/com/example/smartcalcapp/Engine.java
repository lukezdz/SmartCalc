package com.example.smartcalcapp;

import android.content.Context;

import org.nd4j.linalg.api.ndarray.INDArray;
import org.nd4j.linalg.cpu.nativecpu.NDArray;
import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.MatOfPoint;
import org.opencv.core.MatOfPoint2f;
import org.opencv.core.Point;
import org.opencv.core.Rect;
import org.opencv.core.Scalar;
import org.opencv.core.Size;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Engine {
    public static final String FILENAME = "somefile.jpg";
    private static final int THRESHOLD = 128;
    private final NeuralNetwork neuralNetwork;

    public Engine(Context context) throws IOException {
        neuralNetwork = new NeuralNetwork(context);
    }

    public String getEquation() {
        Mat src = Imgcodecs.imread("");
        Mat srcGray = new Mat();
        Imgproc.cvtColor(src, srcGray, Imgproc.COLOR_BGR2GRAY);
        Imgproc.blur(srcGray, srcGray, new Size(3, 3));

        // using opencv cut image into bounding rects
        List<MatOfPoint> contours = new ArrayList<>();
        Mat hierarchy = new Mat();
        Imgproc.findContours(srcGray, contours, hierarchy, Imgproc.RETR_TREE, Imgproc.CHAIN_APPROX_SIMPLE);

        List<Rect> boundingRectangles = new ArrayList<>();

        // TODO: to find bounding rects -> opencv_imgproc.boundingRect();

        StringBuilder equationBuilder = new StringBuilder();
        // TODO: for every rect:
            // TODO: get data from rect
            // TODO: rescale to 28x28
            // TODO: reshape this to 784x1 NDArray using this.reshape(rescaledImage)
            // TODO: predict single character and add ans to return equation
        // TODO: return equation
        return equationBuilder.toString();
    }

    private INDArray reshape(Mat image) {
        // TODO: fill in values with data from image!!!!
        int [] values = {};
        int [] shape = {784, 1};
        return new NDArray(values, shape, 0);
    }
}
