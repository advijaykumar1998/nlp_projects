"use client"

import { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkBreaks from 'remark-breaks';

export default function Home() {
    const [idea, setIdea] = useState<string>('…loading');

    useEffect(() => {
        const evt = new EventSource('/api');
        let buffer = '';

        evt.onmessage = (e) => {
            buffer += e.data.replace('data: ', '');
            setIdea(buffer);
        };
        evt.onerror = () => {
            console.error('SSE error, closing');
            evt.close();
        };

        return () => { evt.close(); };
    }, []);

    return (
        <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
            <div className="container mx-auto px-4 py-12">
                <div className="text-center mb-8">
                    <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
                        Business Idea Generator
                    </h1>
                    <p className="text-gray-600 dark:text-gray-300 text-lg">
                        AI-powered business ideas for the future
                    </p>
                </div>
                <div className="max-w-4xl mx-auto">
                    <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-lg rounded-2xl shadow-xl p-8 border border-white/20">
                        <div className="prose prose-lg dark:prose-invert max-w-none">
                            <ReactMarkdown
                                remarkPlugins={[remarkGfm, remarkBreaks]}
                                components={{
                                    h1: ({ children }) => <h1 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">{children}</h1>,
                                    h2: ({ children }) => <h2 className="text-xl font-semibold mb-3 text-gray-800 dark:text-gray-200">{children}</h2>,
                                    h3: ({ children }) => <h3 className="text-lg font-medium mb-2 text-gray-700 dark:text-gray-300">{children}</h3>,
                                    p: ({ children }) => <p className="mb-4 text-gray-600 dark:text-gray-400 leading-relaxed">{children}</p>,
                                    ul: ({ children }) => <ul className="mb-4 ml-6 list-disc text-gray-600 dark:text-gray-400">{children}</ul>,
                                    ol: ({ children }) => <ol className="mb-4 ml-6 list-decimal text-gray-600 dark:text-gray-400">{children}</ol>,
                                    li: ({ children }) => <li className="mb-2">{children}</li>,
                                    strong: ({ children }) => <strong className="font-semibold text-gray-900 dark:text-white">{children}</strong>,
                                }}
                            >
                                {idea}
                            </ReactMarkdown>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    );
}
