export const isAuthenticated = () => !!localStorage.getItem("access_token");
export const login = (t) => localStorage.setItem("access_token", t);
export const logout = () => localStorage.removeItem("access_token");
