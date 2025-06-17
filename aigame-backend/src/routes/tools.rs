use super::types::Error;
use ffprobe::ffprobe;
use image::GenericImageView;
use rodio::Source;
use tracing::{error, info};

pub struct ImageInfo {
    pub width: u32,
    pub height: u32,
}

pub struct AudioInfo {
    pub duration_secs: f32,
    pub channels: u16,
    pub sample_rate: u32,
}
pub struct VideoInfo {
    pub width: u32,
    pub height: u32,
    pub duration_secs: f32,
}

pub fn handle_image(file_name: &str) -> Result<ImageInfo, Error> {
    let img = image::open(file_name).map_err(|e| {
        error!("failed to open image: {}", e);
        Error::Io
    })?;
    let (width, height) = img.dimensions();
    Ok(ImageInfo { width, height })
}

pub fn handle_audio(file_name: &str) -> Result<AudioInfo, Error> {
    // Open the audio file
    let file = std::fs::File::open(file_name).map_err(|e| {
        error!("failed to open audio: {}", e);
        Error::Io
    })?;
    let source = rodio::Decoder::new(std::io::BufReader::new(file)).map_err(|e| {
        error!("failed to decode audio: {}", e);
        Error::Format
    })?;

    // Extract audio information
    let channels = source.channels();
    let sample_rate = source.sample_rate();

    // Calculate duration (approximate if streaming source)
    let duration_secs = match source.total_duration() {
        Some(duration) => duration.as_secs_f32(),
        None => 0.0, // For streaming sources or when duration can't be determined
    };

    Ok(AudioInfo {
        duration_secs,
        channels,
        sample_rate,
    })
}

pub fn handle_video(file_name: &str) -> Result<VideoInfo, Error> {
    info!("Processing video file: {}", file_name);
    match ffprobe(file_name) {
        Ok(info) => {
            info!("video info: {:?}", info.clone());
            let duration_secs: f32 = info.format.duration.unwrap().parse().unwrap();
            let video_stream = info
                .streams
                .iter()
                .find(|&s| s.codec_type == Some("video".to_string()))
                .ok_or(Error::Format)?;
            let width = video_stream.width.ok_or(Error::Format)?;
            let height = video_stream.height.ok_or(Error::Format)?;

            Ok(VideoInfo {
                duration_secs,
                width: width as u32,
                height: height as u32,
            })
        }
        Err(e) => {
            error!("failed to get video metadata: {}", e);
            Err(Error::Format)
        }
    }
}
