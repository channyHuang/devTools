#include "widget.h"
#include "ui_widget.h"

#include <QDebug>
#include <QColorDialog>

Widget::Widget(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::Widget)
{
    QGridLayout *colorLayout = new QGridLayout();

    QLabel *redLabel = new QLabel("Red: ");
    red = new QLineEdit();
    red->setText("0");
    red->setValidator(new QIntValidator(0, 255, 0));
    connect(red, &QLineEdit::textChanged, this, &Widget::sltValueChange);
    colorLayout->addWidget(redLabel, 0, 0, 1, 1);
    colorLayout->addWidget(red, 0, 1, 1, 1);

    QLabel *greenLabel = new QLabel("Green: ");
    green = new QLineEdit();
    green->setText("0");
    green->setValidator(new QIntValidator(0, 255, 0));
    connect(green, &QLineEdit::textChanged, this, &Widget::sltValueChange);
    colorLayout->addWidget(greenLabel, 1, 0, 1, 1);
    colorLayout->addWidget(green, 1, 1, 1, 1);

    QLabel *blueLabel = new QLabel("Blue: ");
    blue = new QLineEdit();
    blue->setText("0");
    blue->setValidator(new QIntValidator(0, 255, 0));
    connect(blue, &QLineEdit::textChanged, this, &Widget::sltValueChange);
    colorLayout->addWidget(blueLabel, 2, 0, 1, 1);
    colorLayout->addWidget(blue, 2, 1, 1, 1);

    QLabel *alphaLabel = new QLabel("Alpha: ");
    alpha = new QLineEdit();
    alpha->setText("255");
    alpha->setValidator(new QIntValidator(0, 255, 0));
    connect(alpha, &QLineEdit::textChanged, this, &Widget::sltValueChange);
    colorLayout->addWidget(alphaLabel, 3, 0, 1, 1);
    colorLayout->addWidget(alpha, 3, 1, 1, 1);

    colorHex = new QLineEdit();
    colorHex->setText("000000");
    colorLayout->addWidget(new QLabel("#"));
    colorLayout->addWidget(colorHex, 4, 1, 1, 1);
    connect(colorHex, &QLineEdit::textChanged, this, &Widget::sltHexChange);

    label = new QLabel();
    label->setText("Label");
    label->resize(110, 110);

    pixmap.fill(QColor(red->text().toInt(), green->text().toInt(), blue->text().toInt(), alpha->text().toInt()));
    label->setPixmap(pixmap);

    QColorDialog *colorDialog = new QColorDialog();

    QVBoxLayout *mainLayout = new QVBoxLayout();
    //mainLayout->addLayout(colorLayout);
    //mainLayout->addWidget(label);
    mainLayout->addWidget(colorDialog);

    setLayout(mainLayout);
    ui->setupUi(this);
}

Widget::~Widget()
{
    delete ui;
}

void Widget::fromDecToHex()
{
    nRed = red->text().toInt(nullptr, 10);
    nGreen = green->text().toInt(nullptr, 10);
    nBlue = blue->text().toInt(nullptr, 10);
    QString sHex;
    sHex.sprintf("%02x%02x%02x", nRed, nGreen, nBlue);
    colorHex->setText(sHex);
}

void Widget::sltValueChange()
{
    pixmap.fill(QColor(red->text().toInt(), green->text().toInt(), blue->text().toInt(), alpha->text().toInt()));
    label->setPixmap(pixmap);
    fromDecToHex();
    update();
}

void Widget::sltHexChange()
{
    QString str = colorHex->text();
    if (str.length() != 6) return;
    nRed = str.mid(0, 2).toInt(nullptr, 16);
    red->setText(QString::number(nRed));
    nGreen = str.mid(2, 2).toInt(nullptr, 16);
    green->setText(QString::number(nGreen));
    nBlue = str.mid(4, 2).toInt(nullptr, 16);
    blue->setText(QString::number(nBlue));
    pixmap.fill(QColor(red->text().toInt(), green->text().toInt(), blue->text().toInt(), alpha->text().toInt()));
    label->setPixmap(pixmap);
    update();
}

