-- Create table for tracking media downloads
CREATE TABLE IF NOT EXISTS public.download_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    original_url TEXT NOT NULL,
    platform TEXT,
    title TEXT,
    media_type TEXT,
    requested_quality TEXT,
    resolved_resolution TEXT,
    status TEXT NOT NULL DEFAULT 'success',
    error_message TEXT,
    client_ip TEXT,
    user_agent TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_download_records_platform ON public.download_records(platform);
CREATE INDEX IF NOT EXISTS idx_download_records_created_at ON public.download_records(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_download_records_status ON public.download_records(status);

-- Enable Row Level Security (RLS)
ALTER TABLE public.download_records ENABLE ROW LEVEL SECURITY;

-- Allow inserts from anon and authenticated clients
CREATE POLICY "Allow public insert to download_records"
    ON public.download_records
    FOR INSERT
    TO anon, authenticated
    WITH CHECK (true);

-- Allow reading download records
CREATE POLICY "Allow public select download_records"
    ON public.download_records
    FOR SELECT
    TO anon, authenticated
    USING (true);

