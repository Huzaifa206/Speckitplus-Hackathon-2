/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable static export for containerized deployment
  output: 'export',

  // Disable image optimization for static export
  images: {
    unoptimized: true,
  },

  // Note: API calls will use NEXT_PUBLIC_API_URL environment variable
  // No rewrites needed in static export mode
}

module.exports = nextConfig