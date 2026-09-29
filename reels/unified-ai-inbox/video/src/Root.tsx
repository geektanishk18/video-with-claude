import React from 'react';
import {Composition} from 'remotion';
import {Reel} from './Reel';
import {E, FPS} from './lib';
export const Root: React.FC = () => (
  <Composition id="Reel" component={Reel} durationInFrames={Math.ceil(E.total * FPS)} fps={FPS} width={1080} height={1920} />
);
