// Client-side token store. localStorage is acceptable for the MVP (see TD-006 —
// the refresh token especially should move to an httpOnly cookie when auth hardens).
const ACCESS_KEY = "hi_access_token";
const REFRESH_KEY = "hi_refresh_token";

function read(key: string): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem(key);
}

export const authStore = {
  getAccess: (): string | null => read(ACCESS_KEY),
  getRefresh: (): string | null => read(REFRESH_KEY),
  set(access: string, refresh: string): void {
    if (typeof window === "undefined") return;
    window.localStorage.setItem(ACCESS_KEY, access);
    window.localStorage.setItem(REFRESH_KEY, refresh);
  },
  clear(): void {
    if (typeof window === "undefined") return;
    window.localStorage.removeItem(ACCESS_KEY);
    window.localStorage.removeItem(REFRESH_KEY);
  },
};
