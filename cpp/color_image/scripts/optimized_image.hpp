#include <iostream>
#include <sys/ioctl.h>
#include <unistd.h>
#include <errno.h>

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

namespace cv_opt {
    static int render_image_opt(Mat image, bool BY_HEIGHT, const float diff) {

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

            int last_rgb[3] = {255, 255, 255};

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

                if (red_same && green_same && blue_same)
                    cout << "\x1b[38;2;" << to_string(last_rgb[0]) << ";" << to_string(last_rgb[1]) << ";" << to_string(last_rgb[2]) << "m0";
                else {
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
