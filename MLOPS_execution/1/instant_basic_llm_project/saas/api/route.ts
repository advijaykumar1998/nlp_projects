export async function GET() {
  try {
    const groqApiKey = process.env.GROQ_API_KEY;
    console.log('Environment variables available:', Object.keys(process.env).filter(k => k.includes('GROQ') || k.includes('groq')));
    console.log('GROQ_API_KEY value:', groqApiKey ? 'SET' : 'NOT SET');
    
    if (!groqApiKey) {
      return new Response('GROQ_API_KEY not configured. Available env vars: ' + Object.keys(process.env).filter(k => k.includes('GROQ') || k.includes('groq')).join(', '), { status: 500 });
    }

    const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${groqApiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'mixtral-8x7b-32768',
        messages: [
          {
            role: 'user',
            content: 'Come up with a new business idea for AI Agents. Be concise (2-3 sentences).',
          },
        ],
        temperature: 0.7,
        max_tokens: 500,
      }),
    });

    if (!response.ok) {
      return new Response(`Groq API error: ${response.statusText}`, { status: 500 });
    }

    const data = await response.json();
    return new Response(data.choices[0].message.content, { status: 200 });
  } catch (error) {
    console.error(error);
    return new Response('Error generating idea', { status: 500 });
  }
}
