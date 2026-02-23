package org.example;

import java.util.Comparator;

public class BubbleSort {

    static void bubbleSort(int[] arr, int n) {
        for (int j = 0; j < n - 1; j++) {
            boolean swapped = false;
            for (int i = 0; i < n - j - 1; i++) {
                if (arr[i] > arr[i + 1]) {
                    int tmp = arr[i]; arr[i] = arr[i + 1]; arr[i + 1] = tmp;
                    swapped = true;
                }
            }
            if (!swapped) break;
        }
    }

    static void printArray(int[] arr, int size) {
        for (int i = 0; i < size; i++) System.out.print(arr[i] + " ");
        System.out.println();
    }

    static <T> void bubbleSort(T[] arr, Comparator<T> cmp) {
        int n = arr.length;
        for (int j = 0; j < n - 1; j++) {
            boolean swapped = false;
            for (int i = 0; i < n - j - 1; i++) {
                if (cmp.compare(arr[i], arr[i + 1]) > 0) {
                    T tmp = arr[i]; arr[i] = arr[i + 1]; arr[i + 1] = tmp;
                    swapped = true;
                }
            }
            if (!swapped) break;
        }
    }
}

