﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Unsubscriber
{
    public partial class Unsubscriber : Form
    {
        public Unsubscriber()
        {
            InitializeComponent();
        }

        private void bunifuCustomLabel1_Click(object sender, EventArgs e)
        {

        }

        private void bunifuCustomLabel6_Click(object sender, EventArgs e)
        {

        }

        private void bunifuMaterialTextbox2_OnValueChanged(object sender, EventArgs e)
        {
           
        }

        private void bunifuMaterialTextbox1_OnValueChanged(object sender, EventArgs e)
        {

        }

        private void bunifuMaterialTextbox2_MouseClick(object sender, MouseEventArgs e)
        {
        }

        private void GmailPass_Enter(object sender, EventArgs e)
        {
            if (GmailPass.Text == "Password")
            {
                GmailPass.Text = "";
                GmailPass.ForeColor = Color.FromArgb(64, 64, 64); ;
                GmailPass.isPassword = true;
                passShow.Image = Properties.Resources.hide__1_;
            }
           
        }

        private void GmailPass_Leave(object sender, EventArgs e)
        {
            if (GmailPass.Text == "")
            {
                GmailPass.Text = "Password";
                GmailPass.ForeColor = Color.Gray;
                GmailPass.isPassword = false;
                passShow.Image = Properties.Resources.view__1_;
            }
        }

        private void GmailEmail_Enter(object sender, EventArgs e)
        {
            if (GmailEmail.Text == "Email")
            {
                GmailEmail.Text = "";
                GmailEmail.ForeColor = Color.FromArgb(64, 64, 64);
            }
        }

        private void GmailEmail_Leave(object sender, EventArgs e)
        {
            if (GmailEmail.Text == "")
            {
                GmailEmail.Text = "Email";
                GmailEmail.ForeColor = Color.Gray;
            }
        }

        Boolean showpass = false;
        private void passShow_Click(object sender, EventArgs e)
        {
            if (GmailPass.Text != "Password" || GmailPass.Text != "")
            {
                if (showpass == true)
                {
                    passShow.Image = Properties.Resources.hide__1_;
                    showpass = false;
                    GmailPass.isPassword = true;
                }
                else
                {
                    passShow.Image = Properties.Resources.view__1_;
                    showpass = true;
                    GmailPass.isPassword = false;
                }
            }
        }

        private void bunifuCustomLabel3_Click(object sender, EventArgs e)
        {

        }

        private void bunifuCheckbox2_OnChange(object sender, EventArgs e)
        {

        }

        private void bunifuCustomLabel5_Click(object sender, EventArgs e)
        {

        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void KeyWords_Enter(object sender, EventArgs e)
        {
            if (KeyWords.Text == "Key words i.e.  example@vip.kogan.com,")
            {
                KeyWords.Text = "";
                KeyWords.ForeColor = Color.FromArgb(64, 64, 64);
            }
        }

        private void KeyWords_Leave(object sender, EventArgs e)
        {
            if (KeyWords.Text == "")
            {
                KeyWords.Text = "Key words i.e.  example@vip.kogan.com,";
                KeyWords.ForeColor = Color.Gray;
            }
        }

        int[] keys = new int[500];
        int cnt = -1;

        private void KeyWords_OnValueChanged(object sender, EventArgs e)
        {
            if (KeyWords.Text != "")
            {

                if (KeyWords.Text[KeyWords.Text.Length - 1].ToString() == "," && KeyWords.Text != "Key words i.e.  example@vip.kogan.com,")
                {
                    if (KeyWords.Text.Length > 3)
                    {
                        cnt++;
                        if (cnt > 0)
                        {
                            keys[cnt] = keys[cnt - 1] + KeyWords.Text.Length - 1;
                        }
                        else
                        {
                            keys[cnt] = KeyWords.Text.Length - 1;
                        }
                        keyStore.Text = keyStore.Text +"   " + KeyWords.Text;
                    }
                    
                    KeyWords.Text = "";

                }else if(KeyWords.Text[KeyWords.Text.Length - 1].ToString() == "-" && keyStore.Text.Length > 3)
                {
                    Console.WriteLine(keys[cnt]);

                    keyStore.Text = keyStore.Text.Substring(keys[cnt],0);
                    cnt--;
                    KeyWords.Text = "";
                }
            }
        }

        private void GmailPass_OnValueChanged(object sender, EventArgs e)
        {

        }



        private void button1_Click(object sender, EventArgs e)
        {
            string userData = "{\"Email\":\""+ GmailEmail.Text + "\""+ ",\"Password\":\"" + GmailPass.Text + "\"" + ",\"Workplace\":{\"Inbox\":\"" + inboxBTN.Checked + "\"" +
                ",\"Spam\":\"" + spamBTN.Checked+ "\""+",\"All_Mail\":\"" + allmailBTN.Checked + "\"" + ",\"Block\":\"" + blockBTN.Checked+ "\"" + ",\"Delete\":\"" + deleteBTN.Checked+ "\"" +
                ",\"KeyTags\":\"" + keyStore.Text+ "\"" + "}}";


            System.IO.StreamWriter file = new System.IO.StreamWriter(@"userData.json");
            file.Write(userData);
            file.Close();

            Container.Height = 600;
            Unsubscribe.Visible = false;
            keyTagField.Visible = false;
            KeyWords.Visible = false;
            bunifuCustomLabel9.Visible = false;
            bunifuCustomLabel8.Visible = false;
            bunifuCustomLabel2.Visible = false;
            deleteBTN.Visible = false;
            bunifuCustomLabel10.Visible = false;
            bunifuCustomLabel1.Visible = false;
            blockBTN.Visible = false;
            bunifuCustomLabel7.Visible = false;
            spamBTN.Visible = false;
            bunifuCustomLabel3.Visible = false;
            bunifuCustomLabel4.Visible = false;
            inboxBTN.Visible = false;
            bunifuCustomLabel5.Visible = false;
            passShow.Visible = false;
            GmailPass.Visible = false;
            allmailBTN.Visible = false;
            bunifuCustomLabel11.Visible = false;
            GmailEmail.Visible = false;
            pictureBox1.Height = 181;
            pictureBox1.Width = 183;
            pictureBox1.Image = Properties.Resources.loader;
            pictureBox1.Left = 142;
            pictureBox1.Top = 117;
            bunifuCustomLabel6.Font = new Font("Roboto", 14);
            bunifuCustomLabel6.Left = 170;
            bunifuCustomLabel6.Top = 300;
            bunifuProgressBar1.Visible = true;

        }

        private void Container_Paint(object sender, PaintEventArgs e)
        {

        }
    }
}
