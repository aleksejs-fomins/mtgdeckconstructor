#include "mtg_ui.h"
#include "ui_mtg_ui.h"

MTG_UI::MTG_UI(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MTG_UI)
{
    ui->setupUi(this);
}

MTG_UI::~MTG_UI()
{
    delete ui;
}
