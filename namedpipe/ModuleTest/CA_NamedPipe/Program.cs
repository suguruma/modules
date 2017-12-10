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

namespace CA_NamedPipe
{
    class Program
    {
        private static async Task Server()
        {

            // "testpipe"という名前のパイプのサーバ
            using (var stream = new NamedPipeServerStream("testpipe"))
            {
                // クライアントからの接続を待つ
                stream.WaitForConnection();
                // メッセージを受信（読み込み）
                using (var reader = new StreamReader(stream))
                {
                    Console.WriteLine("Receive");
                    string message = await reader.ReadLineAsync();
                    Console.WriteLine($"Received: {message}");
                }
            }
        }
        private static void Server1()
        {
            // Open the named pipe.
            var server = new NamedPipeServerStream("NPtest");

            Console.WriteLine("Waiting for connection...");
            server.WaitForConnection();

            Console.WriteLine("Connected.");
            var br = new BinaryReader(server);
            var bw = new BinaryWriter(server);

            while (true)
            {
                try
                {
                    var len = (int)br.ReadUInt32();            // Read string length
                    var str = new string(br.ReadChars(len));    // Read string

                    Console.WriteLine("Read: \"{0}\"", str);

                    str = new string(str.Reverse().ToArray());  // Just for fun

                    var buf = Encoding.ASCII.GetBytes(str);     // Get ASCII byte array     
                    bw.Write((uint)buf.Length);                // Write string length
                    bw.Write(buf);                              // Write string
                    Console.WriteLine("Wrote: \"{0}\"", str);
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

        static void Main(string[] args)
        {
            //Form Form1 = new Form();
            //Form1.Show();
            Server1();
                        
            for (int i = 0; i < 100; i++)
            {
                //Server().Wait();
            }
        }
    }
}
