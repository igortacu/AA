package org.example;

import java.util.Comparator;

public class QuickSort {

    // median-of-three: picks median of arr[low], arr[mid], arr[high] and moves it to arr[high]
    static int medianOfThree(int[] arr, int low, int high) {
        int mid = low + (high - low) / 2;
        if (arr[low] > arr[mid])  swap(arr, low, mid);
        if (arr[low] > arr[high]) swap(arr, low, high);
        if (arr[mid] > arr[high]) swap(arr, mid, high);
        // arr[mid] is the median; put it at high-1 as the pivot
        swap(arr, mid, high);
        return arr[high];
    }

    static int partition(int[] arr, int low, int high) {
        if (high - low >= 2) medianOfThree(arr, low, high);
        int pivot = arr[high];
        int i = low - 1;
        for (int j = low; j < high; j++) {
            if (arr[j] < pivot) {
                i++;
                swap(arr, i, j);
            }
        }
        swap(arr, i + 1, high);
        return i + 1;
    }

    static void swap(int[] arr, int i, int j) {
        int tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
    }

    static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pi = partition(arr, low, high);
            quickSort(arr, low, pi - 1);
            quickSort(arr, pi + 1, high);
        }
    }

    static <T> void swap(T[] arr, int i, int j) {
        T tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
    }

    static <T> int medianOfThree(T[] arr, int low, int high, Comparator<T> cmp) {
        int mid = low + (high - low) / 2;
        if (cmp.compare(arr[low], arr[mid]) > 0)  swap(arr, low, mid);
        if (cmp.compare(arr[low], arr[high]) > 0) swap(arr, low, high);
        if (cmp.compare(arr[mid], arr[high]) > 0) swap(arr, mid, high);
        swap(arr, mid, high);
        return high;
    }

    static <T> int partition(T[] arr, int low, int high, Comparator<T> cmp) {
        if (high - low >= 2) medianOfThree(arr, low, high, cmp);
        T pivot = arr[high];
        int i = low - 1;
        for (int j = low; j < high; j++) {
            if (cmp.compare(arr[j], pivot) <= 0) {
                i++;
                swap(arr, i, j);
            }
        }
        swap(arr, i + 1, high);
        return i + 1;
    }

    static <T> void quickSort(T[] arr, int low, int high, Comparator<T> cmp) {
        if (low < high) {
            int pi = partition(arr, low, high, cmp);
            quickSort(arr, low, pi - 1, cmp);
            quickSort(arr, pi + 1, high, cmp);
        }
    }
}

