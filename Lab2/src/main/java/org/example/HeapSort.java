package org.example;

import java.util.Comparator;

public class HeapSort {

    static void heapify(int[] arr, int n, int i) {
        int largest = i, l = 2 * i + 1, r = 2 * i + 2;
        if (l < n && arr[l] > arr[largest]) largest = l;
        if (r < n && arr[r] > arr[largest]) largest = r;
        if (largest != i) {
            int tmp = arr[i]; arr[i] = arr[largest]; arr[largest] = tmp;
            heapify(arr, n, largest);
        }
    }

    static void heapSort(int[] arr) {
        int n = arr.length;
        for (int i = n / 2 - 1; i >= 0; i--) heapify(arr, n, i);
        for (int i = n - 1; i >= 0; i--) {
            int tmp = arr[0]; arr[0] = arr[i]; arr[i] = tmp;
            heapify(arr, i, 0);
        }
    }

    static <T> void heapify(T[] arr, int n, int i, Comparator<T> cmp) {
        int largest = i, l = 2 * i + 1, r = 2 * i + 2;
        if (l < n && cmp.compare(arr[l], arr[largest]) > 0) largest = l;
        if (r < n && cmp.compare(arr[r], arr[largest]) > 0) largest = r;
        if (largest != i) {
            T tmp = arr[i]; arr[i] = arr[largest]; arr[largest] = tmp;
            heapify(arr, n, largest, cmp);
        }
    }

    static <T> void heapSort(T[] arr, Comparator<T> cmp) {
        int n = arr.length;
        for (int i = n / 2 - 1; i >= 0; i--) heapify(arr, n, i, cmp);
        for (int i = n - 1; i >= 0; i--) {
            T tmp = arr[0]; arr[0] = arr[i]; arr[i] = tmp;
            heapify(arr, i, 0, cmp);
        }
    }
}

