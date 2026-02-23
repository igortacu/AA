package org.example;

import java.util.Arrays;
import java.util.Random;

public class Main {

    static final int[] SIZES = {250, 500, 750, 1000, 1500, 2000, 3000, 4000, 5000, 7500, 10000, 15000, 20000};
    static final int[] SIZES_NO_BUBBLE = {500, 1000, 2000, 5000, 10000, 20000, 40000, 60000, 80000, 100000};
    static final int RUNS = 5;
    static final Random RNG = new Random(42);

    static int[] randomArray(int n) {
        int[] a = new int[n];
        for (int i = 0; i < n; i++) a[i] = RNG.nextInt(100_000);
        return a;
    }

    static int[] sortedArray(int n) {
        int[] a = new int[n];
        for (int i = 0; i < n; i++) a[i] = i;
        return a;
    }

    static int[] reverseSortedArray(int n) {
        int[] a = new int[n];
        for (int i = 0; i < n; i++) a[i] = n - i;
        return a;
    }

    interface SortFn { void sort(int[] arr); }

    // runs fn RUNS times on a copy of original, returns avg time in ms
    static double timeSort(SortFn fn, int[] original) {
        long total = 0;
        for (int r = 0; r < RUNS; r++) {
            int[] copy = Arrays.copyOf(original, original.length);
            long start = System.nanoTime();
            fn.sort(copy);
            total += System.nanoTime() - start;
        }
        return (total / (double) RUNS) / 1_000_000.0;
    }

    static double[][] analyse(String inputType, int[] sizes, int[][] inputs) {
        System.out.printf("%n--- %s (avg over %d runs) ---%n", inputType, RUNS);
        System.out.printf("%-10s %12s %12s %12s %12s%n", "Size", "QuickSort", "MergeSort", "HeapSort", "BubbleSort");

        double[][] results = new double[4][sizes.length];

        for (int i = 0; i < sizes.length; i++) {
            int[] base = inputs[i];

            double tQuick  = timeSort(a -> QuickSort.quickSort(a, 0, a.length - 1), base);
            double tMerge  = timeSort(a -> MergeSort.mergeSort(a, 0, a.length - 1), base);
            double tHeap   = timeSort(HeapSort::heapSort, base);
            double tBubble = timeSort(a -> BubbleSort.bubbleSort(a, a.length), base);

            results[0][i] = tQuick;
            results[1][i] = tMerge;
            results[2][i] = tHeap;
            results[3][i] = tBubble;

            System.out.printf("%-10d %12.4f %12.4f %12.4f %12.4f%n",
                    sizes[i], tQuick, tMerge, tHeap, tBubble);
        }

        return results;
    }

    static void verifyCorrectness() {
        System.out.println("\n--- Correctness check ---");
        int[] original = {64, 34, 25, 12, 22, 11, 90, 1, 77, 45};
        int[] expected = Arrays.copyOf(original, original.length);
        Arrays.sort(expected);

        String[] names = {"QuickSort", "MergeSort", "HeapSort", "BubbleSort"};
        SortFn[] fns = {
            a -> QuickSort.quickSort(a, 0, a.length - 1),
            a -> MergeSort.mergeSort(a, 0, a.length - 1),
            HeapSort::heapSort,
            a -> BubbleSort.bubbleSort(a, a.length)
        };

        for (int i = 0; i < fns.length; i++) {
            int[] copy = Arrays.copyOf(original, original.length);
            fns[i].sort(copy);
            boolean ok = Arrays.equals(copy, expected);
            System.out.printf("  %-12s %s%n", names[i], ok ? "PASS" : "FAIL got: " + Arrays.toString(copy));
        }
    }

    public static void main(String[] args) {
        // inputs for the full set (includes BubbleSort)
        int[][] randomInputs   = new int[SIZES.length][];
        int[][] sortedInputs   = new int[SIZES.length][];
        int[][] reversedInputs = new int[SIZES.length][];
        for (int i = 0; i < SIZES.length; i++) {
            randomInputs[i]   = randomArray(SIZES[i]);
            sortedInputs[i]   = sortedArray(SIZES[i]);
            reversedInputs[i] = reverseSortedArray(SIZES[i]);
        }

        // larger inputs without BubbleSort (too slow)
        int[][] randomLarge   = new int[SIZES_NO_BUBBLE.length][];
        int[][] sortedLarge   = new int[SIZES_NO_BUBBLE.length][];
        int[][] reversedLarge = new int[SIZES_NO_BUBBLE.length][];
        for (int i = 0; i < SIZES_NO_BUBBLE.length; i++) {
            randomLarge[i]   = randomArray(SIZES_NO_BUBBLE[i]);
            sortedLarge[i]   = sortedArray(SIZES_NO_BUBBLE[i]);
            reversedLarge[i] = reverseSortedArray(SIZES_NO_BUBBLE[i]);
        }

        verifyCorrectness();
        EdgeCaseAnalyzer.run();

        double[][] rRandom   = analyse("RANDOM",         SIZES, randomInputs);
        double[][] rSorted   = analyse("SORTED",         SIZES, sortedInputs);
        double[][] rReversed = analyse("REVERSE_SORTED", SIZES, reversedInputs);

        // no-bubble runs (3 algorithms only, rows 0-2)
        double[][] rRandomNB   = analyse("RANDOM (no bubble)",         SIZES_NO_BUBBLE, randomLarge);
        double[][] rSortedNB   = analyse("SORTED (no bubble)",         SIZES_NO_BUBBLE, sortedLarge);
        double[][] rReversedNB = analyse("REVERSE_SORTED (no bubble)", SIZES_NO_BUBBLE, reversedLarge);

        String[] all3    = {"QuickSort", "MergeSort", "HeapSort", "BubbleSort"};
        String[] fast3   = {"QuickSort", "MergeSort", "HeapSort"};

        // per-algorithm: how it behaves across all 3 input types
        double[][] quickByType    = {rRandom[0],   rSorted[0],   rReversed[0]};
        double[][] mergeByType    = {rRandom[1],   rSorted[1],   rReversed[1]};
        double[][] heapByType     = {rRandom[2],   rSorted[2],   rReversed[2]};
        double[][] bubbleByType   = {rRandom[3],   rSorted[3],   rReversed[3]};
        String[]   inputTypeNames = {"Random", "Sorted", "Reverse-Sorted"};

        try {
            // --- Chart 1-3: all 4 algorithms per input type (up to n=20k) ---
            ChartGenerator.saveChart("All algorithms – Random input",         SIZES, rRandom,   all3, "charts/all_random.png");
            ChartGenerator.saveChart("All algorithms – Sorted input",         SIZES, rSorted,   all3, "charts/all_sorted.png");
            ChartGenerator.saveChart("All algorithms – Reverse-sorted input", SIZES, rReversed, all3, "charts/all_reversed.png");

            // --- Chart 4-6: fast algorithms only, larger range (up to n=100k) ---
            ChartGenerator.saveChart("QuickSort / MergeSort / HeapSort – Random input",         SIZES_NO_BUBBLE, trim3(rRandomNB),   fast3, "charts/fast_random.png");
            ChartGenerator.saveChart("QuickSort / MergeSort / HeapSort – Sorted input",         SIZES_NO_BUBBLE, trim3(rSortedNB),   fast3, "charts/fast_sorted.png");
            ChartGenerator.saveChart("QuickSort / MergeSort / HeapSort – Reverse-sorted input", SIZES_NO_BUBBLE, trim3(rReversedNB), fast3, "charts/fast_reversed.png");

            // --- Chart 7-10: per-algorithm across input types ---
            ChartGenerator.saveChart("QuickSort – behaviour by input type",    SIZES, quickByType,  inputTypeNames, "charts/per_alg_quick.png");
            ChartGenerator.saveChart("MergeSort – behaviour by input type",    SIZES, mergeByType,  inputTypeNames, "charts/per_alg_merge.png");
            ChartGenerator.saveChart("HeapSort – behaviour by input type",     SIZES, heapByType,   inputTypeNames, "charts/per_alg_heap.png");
            ChartGenerator.saveChart("BubbleSort – behaviour by input type",   SIZES, bubbleByType, inputTypeNames, "charts/per_alg_bubble.png");

            System.out.println("\nCharts saved to charts/");
        } catch (Exception e) {
            System.err.println("Chart generation failed: " + e.getMessage());
        }
    }

    // keep only first 3 rows (drop BubbleSort row) from a 4-row result matrix
    static double[][] trim3(double[][] m) {
        return new double[][]{ m[0], m[1], m[2] };
    }
}
