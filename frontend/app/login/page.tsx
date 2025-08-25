"use client";

import {useState} from "react";
import axios from "axios";

export default function LoginPage(){
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [token, setToken] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleLogin = async () => {
        setError("");
        setLoading(true);
        try {
            const response = await axios.post("http://localhost:8000/users/v1/login", {username, password});

            setToken(response.data.access_token);
            console.log(response.data.access_token);
        }
        catch(err: any) {
    if (err.response) {
        console.log("Backend error:", err.response.status, err.response.data);
    } else if (err.request) {
        console.log("No response from backend", err.request);
    } else {
        console.log("Frontend error:", err.message);
    }
}
    };
    return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
      <div className="bg-white p-8 rounded shadow-md w-full max-w-sm">
        <h1 className="text-2xl font-bold text-center mb-6 text-purple-700">Login</h1>
        {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
          className="w-full p-2 mb-4 border border-gray-300 rounded focus:outline-none focus:border-purple-500"
        />
        <input
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          type="password"
          placeholder="Password"
          className="w-full p-2 mb-4 border border-gray-300 rounded focus:outline-none focus:border-purple-500"
        />
        <button
          onClick={handleLogin}
          disabled={loading}
          className="w-full bg-purple-700 text-white py-2 rounded hover:bg-purple-600 disabled:opacity-50"
        >
          {loading ? "Logging in..." : "Login"}
        </button>
        {token && (
          <p className="mt-4 text-xs text-green-600 break-all">
            Token: {token}
          </p>
        )}
      </div>
    </div>
  );

}