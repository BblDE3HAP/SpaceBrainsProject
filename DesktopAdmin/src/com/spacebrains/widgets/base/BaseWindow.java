package com.spacebrains.widgets.base;

import com.spacebrains.core.AppController;
import com.spacebrains.interfaces.INamed;
import com.spacebrains.ui.FormsManager;
import com.spacebrains.core.util.BaseParams;
import com.spacebrains.widgets.AppMenu;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;

import static com.spacebrains.core.util.BaseParams.ALERT_MSG;
import static com.spacebrains.core.util.BaseParams.setDefaultFont;

public abstract class BaseWindow extends JFrame implements WindowListener {

    public boolean wasAlreadyOpenedBefore = false;
    protected String windowTitle = BaseParams.APP_NAME;

    public AppMenu menu;

    protected static final int DEFAULT_WIDTH = 550;
    protected static final int DEFAULT_HEIGHT = 485;

    protected int width = DEFAULT_WIDTH;
    protected int height = DEFAULT_HEIGHT;

    protected Box content;
    protected BaseEditForm<? extends INamed> editDialog;

    public BaseWindow() {
        this(DEFAULT_WIDTH, DEFAULT_HEIGHT);
    }

    public BaseWindow(int width, int height) {
        initMainSettings(width, height);
        setDefaultFont();
        initMainMenu();

        addWindowListener(this);
    }

    private void initMainSettings(int width, int height) {
        this.width = width;
        this.height = height;
        setTitle(windowTitle);
        setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        content = Box.createVerticalBox();
        content.setAlignmentY(Component.CENTER_ALIGNMENT);

        // смотрим размер экрана и размещаем окно чата в центре
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        setBounds((screenSize.width - width) / 2, (screenSize.height - height) / 2, width, height);

        // Приводим внешний вид элементов к виду как в системе пользователя (например соответствующий теме windows)
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception ignore) {}

        add(content);
        setResizable(false);
    }

    private void initMainMenu() {
        menu = new AppMenu();
        setJMenuBar(menu);
        JFrame currentWindow = this;

        menu.getMiDictsPersons().addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                currentWindow.setVisible(false);
                FormsManager.showPersonsDictionaryForm();
            }
        });

        menu.getMiDictsKeywords().addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                currentWindow.setVisible(false);
                FormsManager.showKeywordsDictionaryForm();
            }
        });

        menu.getMiDictsSites().addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                currentWindow.setVisible(false);
                FormsManager.showSitesDictionaryForm();
            }
        });

        menu.getMiFileCrawlerStats().addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                currentWindow.setVisible(false);
                FormsManager.showCrawlerStatsForm();
            }
        });

        menu.getMiFileChangePswd().addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                currentWindow.setVisible(false);
                FormsManager.showChangePswdForm();
            }
        });

        menu.getMiFileLogout().addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                AppController.getInstance().logout();
                currentWindow.setVisible(false);
                FormsManager.showAuthorizationForm();
            }
        });

        menu.getMiDictsUsers().addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                currentWindow.setVisible(false);
                FormsManager.showUsersForm();
            }
        });
    }

    protected int getDeleteConfirmation(JFrame currentFrame, String objectName) {
        Object[] options = {"Да", "Нет"};
        return JOptionPane.showOptionDialog(currentFrame,
                "Вы хотите удалить элемент '" + objectName + "'?",
                ALERT_MSG,
                JOptionPane.YES_NO_OPTION,
                JOptionPane.QUESTION_MESSAGE,
                null,     // без специальной иконки
                options,  // заголовки кнопок
                options[0]); // выбор по умолчанию
    }

    @Override
    public void windowClosing(WindowEvent e) {}

    @Override
    public void windowOpened(WindowEvent e) {}

    @Override
    public void windowClosed(WindowEvent e) {}

    @Override
    public void windowIconified(WindowEvent e) {}

    @Override
    public void windowDeiconified(WindowEvent e) {}

    @Override
    public void windowDeactivated(WindowEvent e) {}

    @Override
    public void windowActivated(WindowEvent e) {
        initMainSettings(width, height);
    }

    protected Component setElementSize(Component component, Dimension dimension) {
        component.setMinimumSize(dimension);
        component.setMaximumSize(dimension);
        component.setPreferredSize(dimension);
        return component;
    }
}
