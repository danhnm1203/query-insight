import * as Sentry from "@sentry/react";

export const initSentry = () => {
    const dsn = import.meta.env.VITE_SENTRY_DSN;
    if (dsn) {
        Sentry.init({
            dsn: dsn,
            integrations: [
                Sentry.browserTracingIntegration(),
                Sentry.replayIntegration(),
            ],
            // Performance Monitoring
            tracesSampleRate: 1.0,
            // Session Replay
            replaysSessionSampleRate: 0.1,
            replaysOnErrorSampleRate: 1.0,
        });
        console.log("✅ Sentry initialized");
    } else {
        console.log("⚠️ Sentry DSN not found, skipping initialization");
    }
};
