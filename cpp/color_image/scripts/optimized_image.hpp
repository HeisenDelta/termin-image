#include <iostream>
#include <sys/ioctl.h>
#include <unistd.h>
#include <errno.h>
#include <cmath>

#include <opencv2/opencv.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace std;
using namespace cv;

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

void rgb_to_hsl(int red, int green, int blue, int &hue, int &sat, int &light) {

    float r_fl = red / 255.0;
    float g_fl = green / 255.0;
    float b_fl = blue / 255.0;

    float c_min = min(r_fl, min(g_fl, b_fl));
    float c_max = max(r_fl, max(g_fl, b_fl));
    light = 50 * (c_min + c_max);

    if (c_min == c_max) {
        hue, sat = 0;
        return;
    }
    else if (light < 50) sat = 100 * (c_max - c_min) / (c_max + c_min);
    else sat = 100 * (c_max - c_min) / (2.0 - c_max - c_min);

    if (c_max == r_fl) hue = 60 * (g_fl - b_fl) / (c_max - c_min);
    if (c_max == g_fl) hue = 60 * (b_fl - r_fl) / (c_max - c_min) + 120;
    if (c_max == b_fl) hue = 60 * (r_fl - g_fl) / (c_max - c_min) + 240;
    if (hue < 0) hue += 360;

}

float hue_to_rgb(int p, int q, int t) {

    if (t < 0) t += 1;
    if (t > 1) t += 1;
    if (t < 1/6) return p + (q - p) * 6 * t;
    if (t < 1/2) return q;
    if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
    return p;

}

void hsl_to_rgb(uchar &red, uchar &green, uchar &blue, int hue, int sat, int light) {

    if (sat == 0) {
        red = round(light * 255);
        blue = round(light * 255);
        green = round(light * 255);
    } else {
        float q = light < 0.5 ? light * (1 + sat) : light + sat - light * sat;
        float p = 2 * light - q;

        red = round(hue_to_rgb(p, q, hue + 1/3) * 255);
        green = round(hue_to_rgb(p, q, hue) * 255);
        blue = round(hue_to_rgb(p, q, hue - 1/3) * 255);
    }

}


namespace cv_opt {
    static int render_image_opt(Mat image, bool BY_HEIGHT, const float diff, int bright = 0) {

        // Get Terminal width and height
        int t_width, t_height;
        if (
            get_terminal_size(STDIN_FILENO, &t_width, &t_height) &&
            get_terminal_size(STDOUT_FILENO, &t_width, &t_height) &&
            get_terminal_size(STDERR_FILENO, &t_width, &t_height)
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

                RGBValue &rgb = image.ptr<RGBValue>(y)[x];
                unsigned long hex_code = convert_to_rgb(rgb.red, rgb.green, rgb.blue);

                uchar min_red = (1 - diff) * last_rgb[0];
                uchar max_red = (1 + diff) * last_rgb[0];
                uchar min_green = (1 - diff) * last_rgb[1];
                uchar max_green = (1 + diff) * last_rgb[1];
                uchar min_blue = (1 - diff) * last_rgb[2];
                uchar max_blue = (1 + diff) * last_rgb[2];

                bool red_same = min_red < rgb.red && max_red > rgb.red;
                bool green_same = min_green < rgb.green && max_green > rgb.green;
                bool blue_same = min_blue < rgb.blue && max_blue > rgb.blue;

                // int hue, sat, light;

                if (red_same && green_same && blue_same) {
                    // rgb_to_hsl(last_rgb[0], last_rgb[1], last_rgb[2], hue, sat, light);
                    // light += bright;
                    // hsl_to_rgb(last_rgb[0], last_rgb[1], last_rgb[2], hue, sat, light);

                    cout << "\x1b[38;2;" << to_string(last_rgb[0]) << ";" << to_string(last_rgb[1]) << ";" << to_string(last_rgb[2]) << "m0";
                } else {
                    // rgb_to_hsl(rgb.red, rgb.green, rgb.blue, hue, sat, light);
                    // light += bright;
                    // hsl_to_rgb(rgb.red, rgb.green, rgb.blue, hue, sat, light);

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
}
