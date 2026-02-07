import { NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';

/**
 * GET /health
 * Liveness probe endpoint - checks if frontend is alive
 * Returns 200 OK if service is running
 */
export async function GET() {
  const startTime = Date.now();
  const uptime = process.uptime();

  return NextResponse.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: Math.floor(uptime),
    version: '1.0.0',
  }, {
    status: 200,
    headers: {
      'Cache-Control': 'no-cache, no-store, must-revalidate',
    },
  });
}
