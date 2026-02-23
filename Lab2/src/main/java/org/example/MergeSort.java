package org.example;

import java.lang.reflect.Array;
import java.util.Comparator;

public class MergeSort {

    static void merge(int[] arr, int l, int m, int r) {
        int n1 = m - l + 1, n2 = r - m;
        int[] L = new int[n1], R = new int[n2];

        for (int i = 0; i < n1; i++) L[i] = arr[l + i];
        for (int j = 0; j < n2; j++) R[j] = arr[m + 1 + j];

        int i = 0, j = 0, k = l;
        while (i < n1 && j < n2) {
            if (L[i] <= R[j]) { arr[k] = L[i]; i++; }
            else               { arr[k] = R[j]; j++; }
            k++;
        }
        while (i < n1) { arr[k] = L[i]; i++; k++; }
        while (j < n2) { arr[k] = R[j]; j++; k++; }
    }

    static void mergeSort(int[] arr, int l, int r) {
        if (l < r) {
            int m = (l + r) / 2;
            mergeSort(arr, l, m);
            mergeSort(arr, m + 1, r);
            merge(arr, l, m, r);
        }
    }

    @SuppressWarnings("unchecked")
    static <T> void merge(T[] arr, int l, int m, int r, Comparator<T> cmp) {
        int n1 = m - l + 1, n2 = r - m;
        T[] L = (T[]) Array.newInstance(arr.getClass().getComponentType(), n1);
        T[] R = (T[]) Array.newInstance(arr.getClass().getComponentType(), n2);

        for (int i = 0; i < n1; i++) L[i] = arr[l + i];
        for (int j = 0; j < n2; j++) R[j] = arr[m + 1 + j];

        int i = 0, j = 0, k = l;
        while (i < n1 && j < n2) {
            if (cmp.compare(L[i], R[j]) <= 0) { arr[k] = L[i]; i++; }
            else                               { arr[k] = R[j]; j++; }
            k++;
        }
        while (i < n1) { arr[k] = L[i]; i++; k++; }
        while (j < n2) { arr[k] = R[j]; j++; k++; }
    }

    static <T> void mergeSort(T[] arr, int l, int r, Comparator<T> cmp) {
        if (l < r) {
            int m = (l + r) / 2;
            mergeSort(arr, l, m, cmp);
            mergeSort(arr, m + 1, r, cmp);
            merge(arr, l, m, r, cmp);
        }
    }
}

