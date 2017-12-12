using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using System.IO.Pipes;

//http://ichiroku11.hatenablog.jp/entry/2016/07/19/222921
namespace WFA_NamedPipe
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            string message = textBox1.Text;
            Client(message).Wait();
        }

        private static async Task Client(string message)
        {
            using (var stream = new NamedPipeClientStream("testpipe"))
            {
                // サーバに接続
                stream.Connect();

                // メッセージを送信
                using (var writer = new StreamWriter(stream))
                {                    
                    await writer.WriteLineAsync(message);
                }
            }
        }

        private async void button2_Click(object sender, EventArgs e)
        {
            //http://kimux.net/?p=902
            this.button2.Enabled = false;
            this.label1.Text = "Connected";

            await Task.Run(() => {
                Server1(this.textBox2.Text, this.numericUpDown1.Value);
            });

            this.button2.Enabled = true;
            this.label1.Text = "Disconnected";
        }

        private static void Server1(string pipename, decimal max_loop)
        {
            // Open the named pipe.
            var server = new NamedPipeServerStream(pipename);
            try
            {
                Console.WriteLine("Waiting for connection...");
                server.WaitForConnection();
                Console.WriteLine("Connected.");
            }
            catch
            {
                server.Close();
                server.Dispose();
            }

            var bw = new BinaryWriter(server);
            int counter = 0;
            Random cRand = new System.Random();

            while (true)
            {
                try
                {
                    int[] arrayNum = new int[45];
                    for (int i =0; i<arrayNum.Length; i++)
                    {
                        arrayNum[i] = cRand.Next(i);
                    }
                    var str = string.Join(",", arrayNum);
                    //'.' + 
                    var buf = Encoding.ASCII.GetBytes(str + "\r\n"); // Get ASCII byte array     
                    //bw.Write((uint)buf.Length);                // Write string length
                    bw.Write(buf);                             // Write string
                    Console.WriteLine("Wrote:{0:D2}  {1}", counter + 1, str);
                    counter++;
                    if (counter > max_loop - 1) break;
                }
                catch (EndOfStreamException)
                {
                    break;                    // When client disconnects
                }
            }
            Console.WriteLine("Client disconnected.");
            server.Close();
            server.Dispose();
        }
    }
}
