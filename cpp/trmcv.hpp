#include <iostream>
#include <sys/ioctl.h>
#include <unistd.h>
#include <errno.h>
#include <thread>
#include <chrono>

#include <opencv2/opencv.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace std;
using namespace cv;

using namespace std::chrono;
using namespace std::chrono_literals;
using namespace std::this_thread;


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

namespace trmcv {

    static int render_image(Mat image, bool BY_HEIGHT) {

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
        
        // cout << size_obj.width << ' ' << size_obj.height << '\n';
        // cout << t_width << ' ' << t_height << '\n';
        // cout << (float) t_width / size_obj.width << ' ' << (float) t_height / size_obj.height << '\n';

        float hbyw = (float) size_obj.height / (float) size_obj.width;
        float wbyh = (float) size_obj.width / (float) size_obj.height;

        if (BY_HEIGHT) resize(image, image, cv::Size((int) (t_width * wbyh / 0.55), t_width), 0, 0, INTER_AREA);
        else resize(image, image, cv::Size(t_height, (int) (t_height * hbyw * 0.55)), 0, 0, INTER_AREA);

        // Change INTER_AREA to INTER_LINEAR for accentuated pixels

        // const string window_name("image_window");
        // namedWindow(window_name);
        // imshow(window_name, image);
        // waitKey(0);

        // FUTURE: center the image if taken by height
        for (int y = 0; y < image.rows; y++) {
            for (int x = 0; x < image.cols; x++) {

                RGBValue &rgb = image.ptr<RGBValue>(y)[x];

                unsigned long hex_code = convert_to_rgb(rgb.red, rgb.green, rgb.blue);
                cout << "\x1b[38;2;" << to_string(rgb.red) << ";" << to_string(rgb.green) << ";" << to_string(rgb.blue) << "m0";

                // Vec3b &pixel_val = image.at<Vec3b>(y, x);
                // cout << "\x1b[38;2;" << to_string(pixel_val[2]) << ";" << to_string(pixel_val[1]) << ";" << to_string(pixel_val[0]) << "m0";

                // cout << '0';

            }
            cout << '\n';
        }
        return 0;
    }

    static int render_video(VideoCapture cap, const int frame_rate) {

        Mat frame;

        if (!cap.isOpened()) {
            cerr << "Video not found\n";
            return 0;
        }

        while (true) {

            cap >> frame;
            if (frame.empty()) break;

            // imshow("Frame", frame);
            render_image(frame, true);
            cout << "\x1B[3J\x1B[H";                                    // "\x1B[2J\x1B[H" doesn't work that well

            // Frame rate is only used for delay between frames
            this_thread::sleep_for(milliseconds(1000 / frame_rate));

        }

        cap.release();
        destroyAllWindows();
        return 0;

    }

}
