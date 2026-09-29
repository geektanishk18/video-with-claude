import {Config} from '@remotion/cli/config';
// Optional: point Remotion at an existing Chromium (e.g. REMOTION_BROWSER=/path/to/chrome). Otherwise Remotion downloads its own.
if (process.env.REMOTION_BROWSER) Config.setBrowserExecutable(process.env.REMOTION_BROWSER);
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(92);
