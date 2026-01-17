import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Proxy API requests to the backend server
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ];
  },
};

export default nextConfig;
