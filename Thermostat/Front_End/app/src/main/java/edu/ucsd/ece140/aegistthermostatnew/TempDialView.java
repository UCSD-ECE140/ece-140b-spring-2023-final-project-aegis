package edu.ucsd.ece140.aegistthermostatnew;

import android.animation.ArgbEvaluator;
import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.LinearGradient;
import android.graphics.Paint;
import android.graphics.Rect;
import android.graphics.RectF;
import android.graphics.Shader;
import android.util.AttributeSet;
import android.view.View;

import java.util.ArrayList;
import java.util.List;

public class TempDialView extends View {


    // Define the start and end colors
    int startColor = Color.BLUE;
    int endColor = Color.RED;  // Red color

    double setTo = 60;
    double indoor = 73;
    double outdoor = 78;

    double humidity = 50;

    double max = 100;
    float size = 1000;
    RectF oval = new RectF((float) (size*0.07), (float) (size*0.07), (float) (size*0.93), (float) (size*0.93));

    List<Rect> textBounds = new ArrayList<>();  // List to hold the bounds of all texts

    // Create an ArgbEvaluator
    ArgbEvaluator evaluator = new ArgbEvaluator();

    public TempDialView(Context context) {
        super(context);
    }

    public TempDialView(Context context, AttributeSet attrs) {
        super(context, attrs);

    }

    @Override
    protected void onSizeChanged(int w, int h, int oldw, int oldh) {
        super.onSizeChanged(w, h, oldw, oldh);

        size = (float) (w);
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        initialize(canvas);
    }

    public void setValue(double inside, double outside, double set, double humidity) {
        this.setTo = set;
        this.indoor = inside;
        this.outdoor = outside;
        this.humidity = humidity;
        textBounds.clear();
        invalidate();
    }

    private void initialize(Canvas canvas){
        // Define the start and end colors
        int startColor = Color.BLUE;
        int endColor = Color.RED;  // Red color

        // Calculate the current color based on the current value
        //float fraction = (float)(value / max);
        //int currentColor = (Integer)evaluator.evaluate(fraction, startColor, endColor);

        Paint paint = new Paint();
        paint.setStyle(Paint.Style.STROKE);
        paint.setStrokeWidth(25);



        // Create a gradient from blue to red
        LinearGradient gradient = new LinearGradient((float) (size*0.10), (float) 0, (float) (size*0.90), 0, startColor, endColor, Shader.TileMode.CLAMP);
        paint.setShader(gradient);

        // Draw the arc with the current color
        canvas.drawArc(oval, 130, 280, false, paint);

        // Let's say the value you want to represent is 50 (out of a max of 100)
        oval = new RectF((float) (size*0.10), (float) (size*0.10), (float) (size*0.84), (float) (size*0.84));

        drawMark(canvas, setTo, Color.BLUE, "Set: ");
        drawMark(canvas, indoor, Color.RED, "In: ");
        drawMark(canvas, outdoor, Color.GRAY, "Out: ");


        Paint textPaint = new Paint();
        textPaint.setColor(Color.BLACK);  // Set your desired color
        textPaint.setTextSize(size/3);  // Set your desired text size
        textPaint.setTextAlign(Paint.Align.CENTER);

        Paint subTextPaint = new Paint();
        subTextPaint.setColor(Color.BLACK);  // Set your desired color
        subTextPaint.setTextSize(size/20);  // Set your desired text size
        subTextPaint.setTextAlign(Paint.Align.CENTER);

        String tempText = " ";
        tempText+=String.valueOf((int) indoor);
        tempText += "°";
        float centerXF = oval.centerX();
        float centerYF = (oval.centerY() - ((textPaint.descent() + textPaint.ascent()) / 2));

        String humText = "Humidity: ";
        humText+=String.valueOf((int) humidity);
        humText += "%";
        float centerXH = oval.centerX();
        float centerYH = (oval.centerY() - ((textPaint.descent() + textPaint.ascent()) / 2))+size/9;

        canvas.drawText(tempText, centerXF, centerYF, textPaint);
        canvas.drawText(humText, centerXH, centerYH, subTextPaint);
    }

    double findDegree(double displayValue){
        if(displayValue<60) displayValue=60;
        if(displayValue>85) displayValue=85;
        displayValue = displayValue-60;

        // Convert the value into an angle (for 80 percent circle)
        double sweepAngle = 280 * (displayValue / 25)+130;
        return sweepAngle;
    }

    double findX(double displayValue){
        double sweepAngle1 = findDegree((float) displayValue);


        // Calculate the x and y position of the dot
        double centerX = oval.centerX();
        double radius = (oval.width() / 2);
        double angleInRadians = Math.toRadians(sweepAngle1);

        double dotX = centerX + radius * Math.cos(angleInRadians);
        return dotX;
    }

    double findY(double displayValue){
        double sweepAngle1 = findDegree((float) displayValue);
        double centerY = oval.centerY();
        double radius = (oval.width() / 2);
        double angleInRadians = Math.toRadians(sweepAngle1);

        double dotY = centerY + radius * Math.sin(angleInRadians);
        return (float) dotY;
    }

    double lineX1(double displayValue){
        double sweepAngle1 = findDegree((float) displayValue);


        // Calculate the x and y position of the dot
        double centerX = oval.centerX();
        double radius = (oval.width() / 2)-30;
        double angleInRadians = Math.toRadians(sweepAngle1);

        double dotX = centerX + radius * Math.cos(angleInRadians);
        return dotX;
    }

    double lineY1(double displayValue){
        double sweepAngle1 = findDegree((float) displayValue);
        double centerY = oval.centerY();
        double radius = (oval.width() / 2)-30;
        double angleInRadians = Math.toRadians(sweepAngle1);

        double dotY = centerY + radius * Math.sin(angleInRadians);
        return (float) dotY;
    }

    double lineX2(double displayValue){
        double sweepAngle1 = findDegree((float) displayValue);


        // Calculate the x and y position of the dot
        double centerX = oval.centerX();
        double radius = (oval.width() / 2)+70;
        double angleInRadians = Math.toRadians(sweepAngle1);

        double dotX = centerX + radius * Math.cos(angleInRadians);
        return dotX;
    }

    double lineY2(double displayValue){
        double sweepAngle1 = findDegree((float) displayValue);
        double centerY = oval.centerY();
        double radius = (oval.width() / 2)+70;
        double angleInRadians = Math.toRadians(sweepAngle1);

        double dotY = centerY + radius * Math.sin(angleInRadians);
        return (float) dotY;
    }

    double textX(double displayValue){
        double sweepAngle1 = findDegree((float) displayValue);


        // Calculate the x and y position of the dot
        double centerX = oval.centerX();
        double radius = (oval.width() / 2)+70;
        double angleInRadians = Math.toRadians(sweepAngle1);

        double dotX = centerX + radius * Math.cos(angleInRadians);
        return dotX;
    }

    double textY(double displayValue){
        double sweepAngle1 = findDegree((float) displayValue);
        double centerY = oval.centerY();
        double radius = (oval.width() / 2)+70;
        double angleInRadians = Math.toRadians(sweepAngle1);

        double dotY = centerY + radius * Math.sin(angleInRadians);
        return (float) dotY;
    }

    void drawMark(Canvas canvas, double value, int aColor, String text){
        // Draw the dot
        Paint dotPaint = new Paint();
        dotPaint.setStrokeWidth(30);
        dotPaint.setColor(aColor);  // Set your desired color
        canvas.drawLine((float)lineX1(value), (float)lineY1(value), (float)lineX2(value), (float)lineY2(value), dotPaint);

        Paint textPaint = new Paint();
        textPaint.setColor(Color.BLACK);  // Set your desired color
        textPaint.setTextSize(size/20);  // Set your desired text size
        textPaint.setTextAlign(Paint.Align.CENTER);


        text+=String.valueOf((int) value);
        text += "°";
        float centerXF = (float)textX(value);
        float centerYF = (float)textY(value);

        int padding = 5;  // Adjust this value as needed
        Rect bounds = new Rect();

        textPaint.getTextBounds(text, 0, text.length(), bounds);
        bounds.inset(-padding, -padding);  // Increase the size of the bounding box
        bounds.offsetTo((int)centerXF, (int)centerYF);

        boolean collides = true;
        while (collides) {
            collides = false;
            for (Rect otherBounds : textBounds) {
                if (Rect.intersects(bounds, otherBounds)) {
                    collides = true;
                    break;
                }
            }
            if (collides) {
                // Move the bounds to the right
                bounds.offset(bounds.width() + padding, 0);
                // Update the center XF position as well
                centerXF += bounds.width() + padding;
            }
        }

// Remove earlier drawText call, and draw after checking collision
        canvas.drawText(text, centerXF, centerYF, textPaint);
        textBounds.add(bounds);  // Add the bounds of the new text to the list


    }
}
