-- Create database (if not exists)
CREATE DATABASE IF NOT EXISTS aigame DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Select the database
USE aigame;

-- Create attachments table (stores user-uploaded files)
CREATE TABLE IF NOT EXISTS attachments (
    id              INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for the file',
    file_name       VARCHAR(50) NOT NULL DEFAULT 'unnamed' COMMENT 'File name',
    file_type       VARCHAR(50) NOT NULL DEFAULT 'ppt' COMMENT 'Default file type is PPT',
    file_extension  VARCHAR(10) NOT NULL DEFAULT 'pptx' COMMENT 'File extension (default is ppt)',
    file_key        VARCHAR(255) NOT NULL COMMENT 'Unique identifier for the file (e.g., S3 or local path)',
    cover           VARCHAR(255) COMMENT 'cover img url',
    valid           BOOL NOT NULL DEFAULT true COMMENT 'File status',
    status          VARCHAR(10) NOT NULL DEFAULT 'uploaded' COMMENT 'File status (default is uploaded)',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation time',
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Update time'
);

-- Create image assets table (stores images from PPT parsing or user uploads)
CREATE TABLE IF NOT EXISTS images (
    id              INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for the image',
    tag             VARCHAR(50) COMMENT 'Asset tag/name',
    file_extension  VARCHAR(10) NOT NULL DEFAULT 'jpg' COMMENT 'File extension (default is jpg)',
    file_key        VARCHAR(255) NOT NULL COMMENT 'File name or unique identifier (e.g., S3 or local path)',
    `top`           FLOAT NOT NULL DEFAULT 0.0 COMMENT 'Position information of the element in the PPT',
    `left`          FLOAT NOT NULL DEFAULT 0.0 COMMENT 'Position information of the element in the PPT',
    width           FLOAT NOT NULL DEFAULT 0.0 COMMENT 'Width of the element in the PPT',
    height          FLOAT NOT NULL DEFAULT 0.0 COMMENT 'Height of the element in the PPT',
    ori_width       INT UNSIGNED NOT NULL COMMENT 'Original image width',
    ori_height      INT UNSIGNED NOT NULL COMMENT 'Original image height',
    valid           BOOL NOT NULL DEFAULT true COMMENT 'File status',
    attach_id       INT NOT NULL COMMENT 'Associated attachment ID (manually managed association)',
    page            INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Associated ppt page ID (manually managed association)',
    source_type     VARCHAR(10) NOT NULL DEFAULT 'upload' COMMENT 'Source of the file: upload or ppt_parse',
    desp            VARCHAR(1000) COMMENT 'Asset description',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation time'
);

-- Create audio assets table (stores audio files from PPT parsing or user uploads)
CREATE TABLE IF NOT EXISTS audios (
    id              INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for the audio',
    tag             VARCHAR(50) COMMENT 'Asset tag/name',
    file_extension  VARCHAR(10) NOT NULL DEFAULT 'mp3' COMMENT 'File extension (default is mp3)',
    file_key        VARCHAR(255) NOT NULL COMMENT 'File name or unique identifier (e.g., S3 or local path)',
    duration_secs   FLOAT NOT NULL COMMENT 'Duration (in seconds)',
    channels        INT UNSIGNED NOT NULL COMMENT 'Number of channels',
    sample_rate     INT UNSIGNED NOT NULL COMMENT 'Sample rate (Hz)',
    valid           BOOL NOT NULL DEFAULT true COMMENT 'File status',
    attach_id       INT NOT NULL COMMENT 'Associated attachment ID (manually managed association)',
    page            INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Associated ppt page ID (manually managed association)',
    source_type     VARCHAR(10) NOT NULL DEFAULT 'upload' COMMENT 'Source of the file: upload or ppt_parse',
    desp            VARCHAR(1000) COMMENT 'Asset description',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation time'
);

-- Create video assets table (stores video files from PPT parsing or user uploads)
CREATE TABLE IF NOT EXISTS videos(
    id              INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for the audio',
    tag             VARCHAR(50) COMMENT 'Video tag/name',
    file_extension  VARCHAR(10) NOT NULL DEFAULT 'mp4' COMMENT 'File extension (default is mp4)',
    file_key        VARCHAR(255) NOT NULL COMMENT 'File name or unique identifier (e.g., S3 or local path)',
    ori_width       INT UNSIGNED NOT NULL COMMENT 'Original video width',
    ori_height      INT UNSIGNED NOT NULL COMMENT 'Original video height',
    duration_secs   FLOAT NOT NULL COMMENT 'Duration (in seconds)',
    valid           BOOL NOT NULL DEFAULT true COMMENT 'File status',
    attach_id       INT NOT NULL COMMENT 'Associated attachment ID (manually managed association)',
    page            INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Associated ppt page ID (manually managed association)',
    source_type     VARCHAR(10) NOT NULL DEFAULT 'upload' COMMENT 'Source of the file: upload or ppt_parse',
    desp            VARCHAR(1000) COMMENT 'Asset description',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation time'
);

-- Create gamecases table (stores game cases)
CREATE TABLE IF NOT EXISTS gamecases (
    id              INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for the game case',
    attach_id       INT NOT NULL COMMENT 'Associated attachment ID (manually managed association)',
    status          VARCHAR(20) NOT NULL DEFAULT 'pending' COMMENT 'Generation status (optional values: pending, processing, completed, failed)',
    file_key        VARCHAR(255) NOT NULL COMMENT 'File name or unique identifier (e.g., S3 or local path)',
    module_id       INT NOT NULL COMMENT 'Module index in attach',
    access_url      VARCHAR(255) COMMENT 'Access URL (optional)',
    valid           BOOL NOT NULL DEFAULT true COMMENT 'Game status',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation time',
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Update time'
);

-- Create chat_records table (stores user chat records)
CREATE TABLE IF NOT EXISTS chat_records (
    id              INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for the chat record',
    file_key        VARCHAR(512) NOT NULL COMMENT 'NDJSON file path (e.g., S3, local path)',
    valid           TINYINT(1) NOT NULL DEFAULT 1 COMMENT 'Whether it is valid',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation time',
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Update time'
);
