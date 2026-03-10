"use client";

import { useAuth } from "@clerk/nextjs";
import axios, { AxiosRequestConfig, AxiosResponse } from "axios";
import { useMemo } from "react";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

export type ApiClient = ReturnType<typeof useApiClient>;

export function useApiClient() {
  const { getToken } = useAuth();

  return useMemo(() => {
    const instance = axios.create({
      baseURL: BACKEND_URL,
      headers: { "Content-Type": "application/json" },
    });

    instance.interceptors.request.use(async (config) => {
      const token = await getToken();
      if (token) config.headers.Authorization = `Bearer ${token}`;
      return config;
    });

    return {
      get<T = unknown>(path: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
        return instance.get<T>(path, config);
      },
      post<T = unknown>(path: string, data?: unknown, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
        return instance.post<T>(path, data, config);
      },
      put<T = unknown>(path: string, data?: unknown, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
        return instance.put<T>(path, data, config);
      },
      patch<T = unknown>(path: string, data?: unknown, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
        return instance.patch<T>(path, data, config);
      },
      delete<T = unknown>(path: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
        return instance.delete<T>(path, config);
      },
    };
  }, [getToken]);
}
