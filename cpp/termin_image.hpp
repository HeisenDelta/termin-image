#include <iostream>
#include <sys/ioctl.h>
#include <unistd.h>
#include <errno.h>
#include <cmath>
#include <thread>
#include <chrono>

#include <opencv2/opencv.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace std;
using namespace cv;

using namespace std::this_thread;
using namespace std::chrono;
using namespace std::chrono_literals;

namespace tSupport {
    // For pixel values
    struct RGBValue {
        uchar blue;
        uchar green;
        uchar red;
    };

    static int get_terminal_size(const int fd, int *const rows, int *const cols) {

        struct winsize sz;
        int result;

        do {
            result = ioctl(fd, TIOCGWINSZ, &sz);
        } while (result == -1 && errno == EINTR);

        if (result == -1) return errno;
        if (rows) *rows = sz.ws_row;
        if (cols) *cols = sz.ws_col;

        return 0;

    }

    unsigned long convert_to_rgb(int red, int green, int blue) {

        return ((red & 0xff) << 24) + ((green & 0xff) << 24) + ((blue & 0xff) << 24);

    }

    void rgb_to_hsl(uchar red, uchar green, uchar blue, float &hue, float &sat, float &light) {

        float R = (int) red / 255.0;
        float G = (int) green / 255.0;
        float B = (int) blue / 255.0;

        float max_ = max(R, max(G, B));
        float min_ = min(R, min(G, B));
        float diff = max_ - min_;
        light = (max_ + min_) / 2;
        
        if (abs(diff) < 0.0001) {
            sat = 0;
            hue = 0;                                                                            // Technically it's undefined
            return;
        }
        if (light <= 0.5) sat = diff / (max_ + min_);
        else sat = diff / (2 - max_ - min_);

        float r_dist = (max_ - R) / diff;
        float g_dist = (max_ - G) / diff;
        float b_dist = (max_ - B) / diff;

        if (R == max_) hue = b_dist - g_dist;
        else if (G == max_) hue = 2 + r_dist - b_dist;
        else hue = 4 + g_dist - r_dist;

        hue *= 60;
        if (hue < 0) hue += 360;

    }

    float hue_to_rgb(float q1, float q2, float hue) {

        if (hue > 360) hue -= 360;
        if (hue < 0) hue += 360;

        if (hue < 60) return q1 + (q2 - q1) * hue / 60;
        else if (hue < 180) return q2;
        else if (hue < 240) return q1 + (q2 - q1) * (240 - hue) / 60;
        else return q1;

    }

    void hsl_to_rgb(uchar &red, uchar &green, uchar &blue, float hue, float sat, float light) {

        float p1, p2;
        if (light <= 0.5) p2 = light * (1 + sat);
        else p2 = light + sat - light * sat;

        p1 = 2 * light - p2;
        if (sat ==  0) {
            red = light * 255;
            green = light * 255;
            blue = light * 255;
        } else {
            red = hue_to_rgb(p1, p2, hue + 120) * 255;
            green = hue_to_rgb(p1, p2, hue) * 255;
            blue = hue_to_rgb(p1, p2, hue - 120) * 255;
        }

    }

    int convert_to_grayscale(int red, int green, int blue) {

        int bnw = int(red * 0.299 + green * 0.587 + blue * 0.144) & 0xff;
        return (bnw << 16) | (bnw << 8) | bnw;

    }
}

namespace tImage {
    const string spectrum = ",:;!=*%#$&0";
    float part_length = 765 / spectrum.length();

    static int render_image(Mat image, bool BY_HEIGHT, float brt = 1.0) {

        // Get Terminal width and height
        int t_width, t_height;
        if (
            tSupport::get_terminal_size(STDIN_FILENO, &t_width, &t_height) &&
            tSupport::get_terminal_size(STDOUT_FILENO, &t_width, &t_height) &&
            tSupport::get_terminal_size(STDERR_FILENO, &t_width, &t_height)
        ) cerr << "Terminal Size function failed\n";

        // Read the image
        if (image.empty()) {
            cerr << "Image not found\n";
            return 0;
        }

        Size size_obj = image.size();

        float hbyw = (float) size_obj.height / (float) size_obj.width;
        float wbyh = (float) size_obj.width / (float) size_obj.height;

        if (BY_HEIGHT) resize(image, image, cv::Size((int) (t_width * wbyh / 0.55), t_width), 0, 0, INTER_AREA);
        else resize(image, image, cv::Size(t_height, (int) (t_height * hbyw * 0.55)), 0, 0, INTER_AREA);
        // Change INTER_AREA to INTER_LINEAR for accentuated pixels

        for (int y = 0; y < image.rows; y++) {

            string space((int) ((t_height - image.cols) / 2), ' ');
            cout << space;

            for (int x = 0; x < image.cols; x++) {

                tSupport::RGBValue &rgb = image.ptr<tSupport::RGBValue>(y)[x];

                unsigned long hex_code = tSupport::convert_to_rgb(rgb.red, rgb.green, rgb.blue);
                cout << "\x1b[38;2;" << to_string(rgb.red * brt) << ";" << to_string(rgb.green * brt) << ";" << to_string(rgb.blue * brt) << "m0";

            }
            cout << space << '\n';
        }
        return 0;
    }

    static int render_image_opt(Mat image, bool BY_HEIGHT, const float diff, float B = 0.0) {

        // Get Terminal width and height
        int t_width, t_height;
        if (
            tSupport::get_terminal_size(STDIN_FILENO, &t_width, &t_height) &&
            tSupport::get_terminal_size(STDOUT_FILENO, &t_width, &t_height) &&
            tSupport::get_terminal_size(STDERR_FILENO, &t_width, &t_height)
        ) cerr << "Terminal Size function failed\n";

        // Read the image
        if (image.empty()) {
            cerr << "Image not found\n";
            return 0;
        }

        Size size_obj = image.size();

        float hbyw = (float) size_obj.height / (float) size_obj.width;
        float wbyh = (float) size_obj.width / (float) size_obj.height;

        if (BY_HEIGHT) resize(image, image, cv::Size((int) (t_width * wbyh / 0.55), t_width), 0, 0, INTER_AREA);
        else resize(image, image, cv::Size(t_height, (int) (t_height * hbyw * 0.55)), 0, 0, INTER_AREA);

        for (int y = 0; y < image.rows; y++) {

            string space((int) ((t_height - image.cols) / 2), ' ');
            cout << space;

            uchar last_rgb[3] = {255, 255, 255};

            for (int x = 0; x < image.cols; x++) {

                tSupport::RGBValue &rgb = image.ptr<tSupport::RGBValue>(y)[x];
                unsigned long hex_code = tSupport::convert_to_rgb(rgb.red, rgb.green, rgb.blue);

                uchar min_red = (1 - diff) * last_rgb[0];
                uchar max_red = (1 + diff) * last_rgb[0];
                uchar min_green = (1 - diff) * last_rgb[1];
                uchar max_green = (1 + diff) * last_rgb[1];
                uchar min_blue = (1 - diff) * last_rgb[2];
                uchar max_blue = (1 + diff) * last_rgb[2];

                bool red_same = min_red < rgb.red && max_red > rgb.red;
                bool green_same = min_green < rgb.green && max_green > rgb.green;
                bool blue_same = min_blue < rgb.blue && max_blue > rgb.blue;

                float hue, sat, light;

                if (red_same && green_same && blue_same) {
                    tSupport::rgb_to_hsl(last_rgb[0], last_rgb[1], last_rgb[2], hue, sat, light);
                    if (light + B > 1.0) light = 1.0;
                    else light += B;
                    tSupport::hsl_to_rgb(last_rgb[0], last_rgb[1], last_rgb[2], hue, sat, light);

                    cout << "\x1b[38;2;" << to_string(last_rgb[0]) << ";" << to_string(last_rgb[1]) << ";" << to_string(last_rgb[2]) << "m0";
                } else {
                    tSupport::rgb_to_hsl(rgb.red, rgb.green, rgb.blue, hue, sat, light);
                    if (light + B > 1.0) light = 1.0;
                    else light += B;
                    tSupport::hsl_to_rgb(rgb.red, rgb.green, rgb.blue, hue, sat, light);

                    cout << "\x1b[38;2;" << to_string(rgb.red) << ";" << to_string(rgb.green) << ";" << to_string(rgb.blue) << "m0";
                    last_rgb[0] = rgb.red;
                    last_rgb[1] = rgb.green;
                    last_rgb[2] = rgb.blue;
                }
            }
            cout << space << '\n';
        }
        return 0;
    }
    
    static int render_image_grayscale(Mat image, bool BY_HEIGHT, bool chars) {

        // Get Terminal width and height
        int t_width, t_height;
        if (
            tSupport::get_terminal_size(STDIN_FILENO, &t_width, &t_height) &&
            tSupport::get_terminal_size(STDOUT_FILENO, &t_width, &t_height) &&
            tSupport::get_terminal_size(STDERR_FILENO, &t_width, &t_height)
        ) {
            cerr << "Terminal Size function failed\n";
            return 0;
        }

        // Read the image
        if (image.empty()) {
            cerr << "Image not found\n";
            return 0;
        }

        Size size_obj = image.size();

        float hbyw = (float) size_obj.height / (float) size_obj.width;
        float wbyh = (float) size_obj.width / (float) size_obj.height;

        if (BY_HEIGHT) resize(image, image, cv::Size((int) (t_width * wbyh / 0.55), t_width), 0, 0, INTER_AREA);
        else resize(image, image, cv::Size(t_height, (int) (t_height * hbyw * 0.55)), 0, 0, INTER_AREA);

        // Change INTER_AREA to INTER_LINEAR for accentuated pixels

        for (int y = 0; y < image.rows; ++y) {

            string space((int) ((t_height - image.cols) / 2), ' ');
            cout << space;

            for (int x = 0; x < image.cols; ++x) {

                tSupport::RGBValue &rgb = image.ptr<tSupport::RGBValue>(y)[x];
                int converted_rgb = tSupport::convert_to_grayscale((int) rgb.red, (int) rgb.green, (int) rgb.blue);
                
                if (chars) {

                    int sum = rgb.red + rgb.green + rgb.blue;
                    cout << spectrum[(int) floor(sum / part_length)];

                } else {

                    int red_ = converted_rgb >> 16;
                    int green_ = (converted_rgb >> 8) & 0xff;
                    int blue_ = converted_rgb & 0xff;
                    cout << "\x1b[38;2;" << to_string(red_) << ";" << to_string(green_) << ";" << to_string(blue_) << "m0";
                }
            }
            cout << space << '\n';
        }
        return 0;
    }
}

namespace tVideo {
    static int render_video(VideoCapture cap, const int frame_rate, float B) {   

        Mat frame;
        if (!cap.isOpened()) {
            cerr << "Video not found\n";
            return 0;
        }

        while (true) {
            cap >> frame;
            if (frame.empty()) break;
            tImage::render_image_opt(frame, true, 0, B);
            cout << "\x1B[3J\x1B[H";                                     // "\x1B[2J\x1B[H" doesn't work that well

            this_thread::sleep_for(milliseconds(1000 / frame_rate));
        }

        cap.release();
        return 0;
    }
}
