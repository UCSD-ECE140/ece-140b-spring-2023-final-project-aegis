package edu.ucsd.ece140.aegistthermostatnew;


import android.animation.ArgbEvaluator;
import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.LinearGradient;
import android.graphics.Paint;
import android.graphics.RectF;
import android.graphics.Shader;
import android.util.AttributeSet;
import android.view.View;

public class EnergyDialView extends View {

    private double value = 0;
    private double max = 100;

    private int[] colors = {Color.parseColor("#006400"), Color.parseColor("#FFFF00"), Color.parseColor("#8B0000")};
    private float[] positions = {0f, 0.5f, 1f};
    private Paint paint;
    private Paint dotPaint;
    private float[] lineCoords;
    private LinearGradient gradient;

    public EnergyDialView(Context context) {
        super(context);
        init();
    }

    public EnergyDialView(Context context, AttributeSet attrs) {
        super(context, attrs);
        init();
    }

    private void init() {
        paint = new Paint();
        paint.setStyle(Paint.Style.STROKE);
        paint.setStrokeWidth(30);

        dotPaint = new Paint();
        dotPaint.setColor(Color.GRAY);
    }

    @Override
    protected void onSizeChanged(int w, int h, int oldw, int oldh) {
        super.onSizeChanged(w, h, oldw, oldh);

        lineCoords = new float[]{50, h / 2, w - 50, h / 2};
        gradient = new LinearGradient(lineCoords[0], lineCoords[1], lineCoords[2], lineCoords[3], colors, positions, Shader.TileMode.CLAMP);
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);

        paint.setShader(gradient);
        canvas.drawLine(lineCoords[0], lineCoords[1], lineCoords[2], lineCoords[3], paint);

        float dotX = (float) (lineCoords[0] + (lineCoords[2] - lineCoords[0]) * (value / max));
        float dotY = lineCoords[1];
        canvas.drawCircle(dotX, dotY, 40, dotPaint);
    }

    public void setValue(double value) {
        this.value = value;
        invalidate();
    }

    public double getValue() {
        return this.value;
    }
}
