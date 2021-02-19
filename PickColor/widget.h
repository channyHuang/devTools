#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>
#include <QLineEdit>
#include <QIntValidator>
#include <QLabel>
#include <QPixmap>
#include <QColor>
#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QGridLayout>
#include <QDoubleValidator>

QT_BEGIN_NAMESPACE
namespace Ui { class Widget; }
QT_END_NAMESPACE

class Widget : public QWidget
{
    Q_OBJECT

public:
    Widget(QWidget *parent = nullptr);
    ~Widget();

public slots:
    void sltValueChange();
    void sltHexChange();

private:
    Ui::Widget *ui;
    QLabel *label;
    QPixmap pixmap = QPixmap(100, 100);
    QLineEdit *red, *green, *blue, *alpha;
    QLineEdit *colorHex;
    int nRed, nGreen, nBlue;

    void fromDecToHex();
};
#endif // WIDGET_H
