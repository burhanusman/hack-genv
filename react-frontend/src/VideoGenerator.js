import React, { useState } from 'react';
import axios from 'axios';
import './VideoGenerator.css';

const VideoGenerator = () => {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [videoSrc, setVideoSrc] = useState('');
  const [generatedText, setGeneratedText] = useState(''); 
  const [images, setImages] = useState([]); 



  const handleSubmit = async () => {
    setLoading(true);
    try {
    const response = await axios.post('http://127.0.0.1:5000', { input }, {
      headers: {
      'Content-Type': 'application/json'
      }
      });
     setVideoSrc(response.data.videoSrc);
     setVideoSrc('sample.mp4');
     setGeneratedText(response.data.facts.join(', ')); // Update this line
     setImages(response.data.images); // Add this line
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  
  return (
    <div className="content-wrapper">
      <div className="video-generator">
        <h1>Generate your own AI video</h1>
        <div className="input-instruction">
          <img src={'./1-black.png'} alt="" />
          <p>Tell us what you want a video about</p>
        </div>
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="e.g. I want to know about Lions"
        />
        <div className="button-container">
          <button onClick={handleSubmit} disabled={loading}>
            {loading ? 'Loading...' : 'Generate'}
          </button>
        </div>
        {loading && <div className="loading-spinner"></div>}
        <div className="media-container">
          {videoSrc && <video src={videoSrc} controls autoPlay />}
          {generatedText && <p className="generated-text">{generatedText}</p>}
          {images.map((imageUrl, index) => <img key={index} src={imageUrl} alt={`Scenery ${index + 1}`} />)}        
        </div>
      </div>
    </div>
  );
};

export default VideoGenerator;