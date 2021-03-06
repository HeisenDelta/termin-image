#include <iostream>
#include <sys/ioctl.h>
#include <unistd.h>
#include <errno.h>

#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

const string spectrum = ",:;!=*%#$&0";
float part_length = 765 / spectrum.length();

// For storing pixel values
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

int convert_to_grayscale(int red, int green, int blue) {

    int bnw = int(red * 0.299 + green * 0.587 + blue * 0.144) & 0xff;
    return (bnw << 16) | (bnw << 8) | bnw;

}

namespace gcvimg {
    static int render_image_grayscale(Mat image, bool BY_HEIGHT, bool chars) {

        // Get Terminal width and height
        int t_width, t_height;
        if (
            get_terminal_size(STDIN_FILENO, &t_width, &t_height) &&
            get_terminal_size(STDOUT_FILENO, &t_width, &t_height) &&
            get_terminal_size(STDERR_FILENO, &t_width, &t_height)
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

                RGBValue &rgb = image.ptr<RGBValue>(y)[x];
                int converted_rgb = convert_to_grayscale((int) rgb.red, (int) rgb.green, (int) rgb.blue);
                
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
