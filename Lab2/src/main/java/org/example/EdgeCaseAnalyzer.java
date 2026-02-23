package org.example;

import java.util.Arrays;
import java.util.Comparator;

public class EdgeCaseAnalyzer {

    // nulls and NaN sort to the end, everything else by natural order
    static final Comparator<Double> SAFE_CMP = (a, b) -> {
        boolean aNaN = (a == null || a.isNaN());
        boolean bNaN = (b == null || b.isNaN());
        if (aNaN && bNaN) return 0;
        if (aNaN) return 1;
        if (bNaN) return -1;
        return Double.compare(a, b);
    };

    record Complex(double real, double imag) {
        double magnitude() { return Math.sqrt(real * real + imag * imag); }

        @Override
        public String toString() {
            return String.format("(%.1f%+.1fi)", real, imag);
        }
    }

    static final Comparator<Complex> COMPLEX_CMP = Comparator.comparingDouble(Complex::magnitude);

    interface GenSortFn<T> { void sort(T[] arr, Comparator<T> cmp); }

    static <T> String runAll(String label, T[] input, Comparator<T> cmp) {
        String[] names = {"QuickSort", "MergeSort", "HeapSort", "BubbleSort"};

        @SuppressWarnings("unchecked")
        GenSortFn<T>[] fns = new GenSortFn[]{
            (arr, c) -> QuickSort.quickSort( (T[]) arr, 0, ((T[]) arr).length - 1, (Comparator<T>) c),
            (arr, c) -> MergeSort.mergeSort( (T[]) arr, 0, ((T[]) arr).length - 1, (Comparator<T>) c),
            (arr, c) -> HeapSort.heapSort(   (T[]) arr,                             (Comparator<T>) c),
            (arr, c) -> BubbleSort.bubbleSort((T[]) arr,                            (Comparator<T>) c),
        };

        StringBuilder sb = new StringBuilder();
        sb.append(String.format("%n  [%s]%n", label));
        sb.append(String.format("  input:  %s%n", Arrays.toString(input)));

        for (int i = 0; i < names.length; i++) {
            T[] copy = Arrays.copyOf(input, input.length);
            String result;
            try {
                fns[i].sort(copy, cmp);
                result = Arrays.toString(copy);
            } catch (Exception e) {
                result = "ERROR: " + e.getClass().getSimpleName() + " - " + e.getMessage();
            }
            sb.append(String.format("  %-12s %s%n", names[i], result));
        }
        return sb.toString();
    }

    public static void run() {
        System.out.println("\n--- Edge-case analysis ---");

        System.out.println(runAll("empty array",
            new Double[]{}, SAFE_CMP));

        System.out.println(runAll("single element",
            new Double[]{42.0}, SAFE_CMP));

        System.out.println(runAll("three elements",
            new Double[]{3.0, 1.0, 2.0}, SAFE_CMP));

        System.out.println(runAll("all identical",
            new Double[]{5.0, 5.0, 5.0, 5.0, 5.0}, SAFE_CMP));

        System.out.println(runAll("large values",
            new Double[]{(double) Integer.MAX_VALUE, 1e15, -1e15, (double) Integer.MIN_VALUE, 0.0},
            SAFE_CMP));

        System.out.println(runAll("negatives and positives",
            new Double[]{-7.0, 3.0, -1.0, 8.0, -4.0, 0.0}, SAFE_CMP));

        System.out.println(runAll("NaN values (NaN goes last)",
            new Double[]{3.0, Double.NaN, 1.0, Double.NaN, 2.0}, SAFE_CMP));

        System.out.println(runAll("null values (null goes last)",
            new Double[]{3.0, null, 1.0, null, 2.0}, SAFE_CMP));

        System.out.println(runAll("mixed null and NaN",
            new Double[]{null, 5.0, Double.NaN, 2.0, null, Double.NaN, 1.0}, SAFE_CMP));

        System.out.println(runAll("complex numbers sorted by magnitude",
            new Complex[]{
                new Complex(3, 4),   // |z| = 5.0
                new Complex(1, 0),   // |z| = 1.0
                new Complex(-2, -2), // |z| ~ 2.83
                new Complex(0, 6),   // |z| = 6.0
                new Complex(1, 1),   // |z| ~ 1.41
            },
            COMPLEX_CMP));
    }
}
