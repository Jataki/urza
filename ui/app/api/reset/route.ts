// ui/app/api/reset/route.ts
import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    
    const response = await fetch('http://localhost:8000/api/reset', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        session_id: body.sessionId
      }),
    });
    
    if (!response.ok) {
      throw new Error(`Error from backend: ${response.status}`);
    }
    
    return NextResponse.json({ status: 'success' });
  } catch (error) {
    console.error('Error resetting conversation:', error);
    return NextResponse.json(
      { error: 'Failed to reset conversation' },
      { status: 500 }
    );
  }
}