import { NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';

/**
 * GET /api/ready
 * Readiness probe endpoint - checks if frontend is ready to serve traffic
 * Returns 200 if frontend is running (backend connectivity checked at runtime)
 */
export async function GET() {
  return NextResponse.json({
    status: 'ready',
    timestamp: new Date().toISOString(),
  }, {
    status: 200,
    headers: {
      'Cache-Control': 'no-cache, no-store, must-revalidate',
    },
  });
}
