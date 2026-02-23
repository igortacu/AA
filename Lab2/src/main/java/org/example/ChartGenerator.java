package org.example;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartUtils;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.NumberAxis;
import org.jfree.chart.axis.NumberTickUnit;
import org.jfree.chart.labels.XYItemLabelGenerator;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.plot.XYPlot;
import org.jfree.chart.renderer.xy.XYLineAndShapeRenderer;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;

import java.awt.*;
import java.awt.geom.Ellipse2D;
import java.io.File;
import java.io.IOException;
import java.text.DecimalFormat;

public class ChartGenerator {

    static final Color[] PALETTE = {
        new Color(31, 119, 180),
        new Color(255, 127, 14),
        new Color(44, 160, 44),
        new Color(214, 39, 40)
    };

    // results[series][sizeIndex] = time in ms
    public static void saveChart(String title, int[] sizes, double[][] results,
                                 String[] seriesNames, String outputPath) throws IOException {
        XYSeriesCollection dataset = new XYSeriesCollection();
        for (int a = 0; a < seriesNames.length; a++) {
            XYSeries series = new XYSeries(seriesNames[a]);
            for (int s = 0; s < sizes.length; s++) series.add(sizes[s], results[a][s]);
            dataset.addSeries(series);
        }

        JFreeChart chart = ChartFactory.createXYLineChart(
                title, "Input size (n)", "Time (ms)", dataset, PlotOrientation.VERTICAL, true, true, false);

        chart.setBackgroundPaint(Color.WHITE);
        chart.getTitle().setFont(new Font("SansSerif", Font.BOLD, 15));

        XYPlot plot = chart.getXYPlot();
        plot.setBackgroundPaint(new Color(248, 248, 248));
        plot.setDomainGridlinePaint(new Color(200, 200, 200));
        plot.setRangeGridlinePaint(new Color(200, 200, 200));
        plot.setDomainGridlinesVisible(true);
        plot.setRangeGridlinesVisible(true);
        plot.setOutlinePaint(Color.GRAY);

        // x-axis: tick at every data point
        NumberAxis xAxis = (NumberAxis) plot.getDomainAxis();
        xAxis.setAutoRangeIncludesZero(false);
        xAxis.setTickUnit(new NumberTickUnit(sizes[sizes.length / 4]));
        xAxis.setTickLabelFont(new Font("SansSerif", Font.PLAIN, 10));
        xAxis.setLabelFont(new Font("SansSerif", Font.BOLD, 12));

        // y-axis: auto range from zero, ms label
        NumberAxis yAxis = (NumberAxis) plot.getRangeAxis();
        yAxis.setAutoRangeIncludesZero(true);
        yAxis.setNumberFormatOverride(new DecimalFormat("0.###"));
        yAxis.setTickLabelFont(new Font("SansSerif", Font.PLAIN, 10));
        yAxis.setLabelFont(new Font("SansSerif", Font.BOLD, 12));

        XYLineAndShapeRenderer renderer = new XYLineAndShapeRenderer(true, true);
        Shape dot = new Ellipse2D.Double(-4, -4, 8, 8);

        // label generator: show the ms value next to each point
        XYItemLabelGenerator labelGen = (ds, series, item) -> {
            double val = ds.getYValue(series, item);
            return val >= 1.0 ? String.format("%.1f", val) : String.format("%.3f", val);
        };

        for (int i = 0; i < seriesNames.length; i++) {
            renderer.setSeriesPaint(i, PALETTE[i % PALETTE.length]);
            renderer.setSeriesStroke(i, new BasicStroke(2.0f));
            renderer.setSeriesShape(i, dot);
            renderer.setSeriesItemLabelGenerator(i, labelGen);
            renderer.setSeriesItemLabelsVisible(i, true);
        }
        renderer.setDefaultItemLabelFont(new Font("SansSerif", Font.PLAIN, 9));
        renderer.setDefaultItemLabelPaint(Color.DARK_GRAY);
        plot.setRenderer(renderer);

        File out = new File(outputPath);
        out.getParentFile().mkdirs();
        ChartUtils.saveChartAsPNG(out, chart, 1100, 650);
        System.out.println("  saved " + out.getPath());
    }
}
