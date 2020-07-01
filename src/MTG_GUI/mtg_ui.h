#ifndef MTG_UI_H
#define MTG_UI_H

#include <QMainWindow>

namespace Ui {
class MTG_UI;
}

class MTG_UI : public QMainWindow
{
    Q_OBJECT

public:
    explicit MTG_UI(QWidget *parent = 0);
    ~MTG_UI();

private:
    Ui::MTG_UI *ui;
};

#endif // MTG_UI_H
