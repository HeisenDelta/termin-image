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

int main( void ) {

    // Get Terminal width and height
    int t_width, t_height;
    if (
        get_terminal_size(STDIN_FILENO, &t_width, &t_height) &&
        get_terminal_size(STDOUT_FILENO, &t_width, &t_height) &&
        get_terminal_size(STDERR_FILENO, &t_width, &t_height)
    ) cerr << "Terminal Size function failed\n";

    // Read the image
    Mat image = imread("/home/heisendelta/Pictures/me1.jpg", IMREAD_COLOR);
    if (image.empty()) {
        cerr << "Image not found\n";
        return 0;
    }

    Size size_obj = image.size();
    
    // cout << size_obj.width << ' ' << size_obj.height << '\n';
    // cout << t_width << ' ' << t_height << '\n';
    // cout << (float) t_width / size_obj.width << ' ' << (float) t_height / size_obj.height << '\n';

    Mat resized_image;

    // Orientation are given in main.py (this is WIDTH)
    float ratio;
    if (size_obj.height > size_obj.width) {

        (float) t_height / (float) size_obj.height > 1 ? ratio = 1.0 : ratio = (float) t_height / (float) size_obj.height;
        resize(image, resized_image, Size(), ratio, ratio * 0.55);

    } else {

        (float) t_width / (float) size_obj.width > 1 ? ratio = 1.0 : ratio = (float) t_width / (float) size_obj.width;
        resize(image, resized_image, Size(), ratio / 0.55, ratio);

    }

    Size new_size_obj = resized_image.size();

    // const string window_name("image_window");
    // namedWindow(window_name);
    // imshow(window_name, resized_image);
    // waitKey(0);

    for (int y = 0; y < resized_image.rows; y++) {
        for (int x = 0; x < resized_image.cols; x++) {

            RGBValue &rgb = resized_image.ptr<RGBValue>(y)[x];

            unsigned long hex_code = convert_to_rgb(rgb.red, rgb.green, rgb.blue);
            cout << "\x1b[38;2;" << to_string(rgb.red) << ";" << to_string(rgb.green) << ";" << to_string(rgb.blue) << "m0";

            // Vec3b &pixel_val = image.at<Vec3b>(y, x);
            // cout << "\x1b[38;2;" << to_string(pixel_val[2]) << ";" << to_string(pixel_val[1]) << ";" << to_string(pixel_val[0]) << "m0";

            // cout << '0';

        }
        cout << '\n';
    }

}

